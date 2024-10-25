import re
import pandas as pd
from dataclasses import dataclass, field
import json
import os
import pkg_resources
from typing import Optional, List, Dict, Union
from .data_loader import DataLoader

pd.options.mode.chained_assignment = None

module_dir = os.path.dirname(__file__)


@dataclass
class ProcessUtils:

    dropna_percent_threshold: float = 50

    label_screens: bool = False
    screen_split: Dict[Union[tuple, str], str] = field(default_factory= 
                               # MSR numbers by which to split screens
                               lambda: {(0, 5863): "THP-1 1K",  
                               (5863, 1e16): "Anborn"})
    ignore_missing_ranges: bool = False
    label_tfs: bool = True
    tf_list: Optional[List[str]] = None
    gene_info_by_acc: Optional[Dict] = None


    def __post_init__(self):
        if self.label_screens:
            if self.screen_split is None:
                raise ValueError("Provide a dictionary to label screens.")
            if not self.ignore_missing_ranges:
                missing_ranges = self._check_missing_ranges()
                if len(missing_ranges) > 0:
                    raise ValueError(f"Missing MSR numbers in screen" \
                                     " dictionary.\nUnable to label MSR" \
                                     " numbers in range(s) {missing_ranges}.\n"
                                     "To ignore missing ranges, " \
                                     "set ignore_missing_ranges=True. Invalid "\
                                      "screen numbers will be labeled 'NaN'."
                                    ) 
        if self.dropna_percent_threshold <= 1.0:
            raise Warning(f"dropna_percent_threshold is a percent. " \
                          "Not a portion. Passing a value of 1 or less will " \
                          "exlude columns unless they are 99%+ not NaN.")
        if self.label_tfs:
            self.tf_list = self.load_tf_list()

    def _drop_nan_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Drop columns from the DataFrame that exceed a specified percentage 
        of NaN values.

        Parameters:
        df (pandas.DataFrame): The input DataFrame from which columns with 
                            too many NaN values will be dropped.

        Returns:
        pandas.DataFrame: The input DataFrame with columns dropped based 
                        on the NaN percentage threshold.
        """
        # Calculate the percentage of NaN values for each column
        nan_percentage = df.isnull().sum() * 100 / len(df)
        
        # Identify columns to drop
        cols_to_drop = nan_percentage[
            nan_percentage >= self.dropna_percent_threshold
        ].index
        
        df.drop(columns=cols_to_drop, inplace=True)
        
        return df

    def load_tf_list(self) -> List[str]:
        """
        Load transcription factors from a JSON file and return a list of 
        keys.

        Returns:
        List[str]: A list of transcription factor keys from the JSON file.
        """
        tf_path = pkg_resources.resource_filename(
            'z_score_target_engagement',
            'data/acc_by_tf_gene.json'
        )
        
        try:
            with open(tf_path, 'r') as file:
                acc_by_tf_gene = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {tf_path} was not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON from the file {tf_path}.")
        
        return list(acc_by_tf_gene.keys())


    @staticmethod
    def load_gene_info():
        gene_info_path = pkg_resources \
            .resource_filename('z_score_target_engagement',
                                'data/gene_info_by_acc.json')
        with open(gene_info_path, 'r') as file:
            return json.load(file)
        
    def _is_tf(self, gene):
        gene_list = gene.split(';')
        return any(gene in self.tf_list for gene in gene_list)

    def _label_tfs(self, df):
        df["Is TF"] = df["Genes"].apply(self._is_tf)
        return df

    def _split_batch_screen(self, df):
        # Split the batch and screen into a two column dataframe
        batch_screen_df = df['batch'].str.split('_', expand=True)
        batch_screen_df.columns = ['batch', 'screen']

        # Drop the original batch column from the dataframe
        df.drop(columns=["batch"], inplace=True)

        # Concatenate the batch_screen df with the original df
        df = pd.concat([df, batch_screen_df], axis=1)

        return df
    

    def _get_batch_compound_names(self, pivot_df, keep_filenames=False):
        batches = pivot_df["Compound"].apply(DataLoader.extract_batch_num)

        if self.label_screens:
            screens = pivot_df["Compound"].apply(self._get_screen)
            batches = batches + "_" + screens
        
        batches.name = "batch"
        pivot_df = pd.concat([pivot_df, batches], axis=1)
        pivot_df["batch"] = pivot_df["batch"].astype('category')

        # If the pivot_df is multiindexed (it will be if the data is peptides)
        # then the Compound column will get renamed when concatenated.
        # If it is multiindexex, rename new batch column to match
        if ("Compound", "", "") in pivot_df.columns:
            pivot_df = pivot_df.rename(columns={("Compound","",""): "Compound"})

        if keep_filenames:
            pivot_df = pivot_df.rename(columns={"Compound": "Filename"})
            pivot_df["Filename"] = pivot_df["Filename"].astype(str)
            pivot_df["Compound"] = pivot_df["Filename"] \
                .apply(self._get_compound_name)
        else:
            pivot_df["Compound"] = pivot_df["Compound"].astype(str)
            pivot_df["Compound"] = pivot_df["Compound"] \
                .apply(self._get_compound_name)
        pivot_df["Compound"] = pivot_df["Compound"].astype("category")
        return pivot_df
    
    def _get_compound_name(self, s: str) -> str:
        """
        Extracts the compound name from the name of the file.
    
        Parameters
        ----------
        s: str
            An entry from the "Filename" column, a path to where 
            the file is located
        
        Returns
        -------
        str
            The name of the treatment compound
        """
        # Look for compounds with the name TAL####
        if "TAL" in s.upper():
            tal_num = re.search(r'TAL\d+(-\d+)?', s)[0]
            # Strip leading zeros if present
            num = int(re.search(r'\d+(-\d+)?', tal_num)[0])
            new_name = "TAL" + str(num)
            return new_name
        elif "DMSO" in s.upper():
            return "DMSO"
        elif "PRTC" in s.upper():
            return "PRTC"
        elif "nuclei" in s.lower():
            return "NUC"
        elif "nuc" in s.lower(): # cases where it is labeled as NUC2
            nuc_num = re.search(r'NUC\d+(-\d+)?', s)
            if nuc_num is None:
                return "NUC"
            else:
                return nuc_num[0]
        elif "dbet" in s.lower():
            return "dBET6"
        elif "FRA" in s.upper():
            return "FRA"
        elif "none" in s.lower():
            return "None"
        else:
            raise Exception(f"Unable to extract compound from filename {s}.")
    
    def _get_screen(self, msr_str):
        if msr_str.startswith("MSR"):
            try:        
                msr = re.search(r'MSR\d+(-\d+)?', msr_str)[0]
            except:
                raise ValueError(f"Unable to match MSR for filename {msr_str}.")
            
            msr = int(re.search(r'\d+(-\d+)?', msr)[0])
        
            for msr_range, screen_name in self.screen_split.items():
                if isinstance(msr_range, tuple):
                    if msr_range[0] <= msr < msr_range[1]:
                        return screen_name
            raise ValueError(f"Unable to determine screen for MSR {str(msr)}.")
        else:
            screen_name = msr_str.split("_")[0]
            try:
                screen = self.screen_split[screen_name]
            except KeyError:
                raise KeyError(f"Screen name {screen_name} not in screen_dict.")
            return screen

    
    def _check_missing_ranges(self):
        quant_keys = [key for key in self.screen_split.keys() \
                      if isinstance(key, tuple)]
        sorted_ranges = sorted(quant_keys)
        missing_ranges = []

        for i in range(len(sorted_ranges) - 1):
            current_end = sorted_ranges[i][1]
            next_start = sorted_ranges[i+1][0]

            if current_end < next_start:
                missing_ranges.append((current_end, next_start))
        return missing_ranges
    
    @staticmethod
    def _convert_encyclopedia_file(data_container):
        gene_info_by_acc = ProcessUtils.load_gene_info()
        # Take an encyclopedia file and convert it to look like a diann file
        rename_dict = {"Peptide": "Precursor.Id",
                       "Protein": "Protein.Ids"}
        df = data_container.raw_df 
        df = df.rename(columns=rename_dict)
        df[["Genes", "Protein.Ids"]] = df["Protein.Ids"] \
            .apply(lambda x: ProcessUtils \
                   ._extract_gene_info(x, gene_info_by_acc))
        data_container.raw_df = df
        data_container.filetype = "diann"
        return data_container
    
    @staticmethod
    def _extract_gene_info(protein_ids, gene_info_by_acc):
        protein_list = protein_ids.split(';')

        gene_ids = set() 
        clean_proteins = [] 
        
        for protein in protein_list:
            if '|' in protein:
                protein_id = protein.split('|')[1]
            else:
                protein_id = protein
                
            base_protein_id = protein_id.split('-')[0]

            base_protein_id = protein_id.split('-')[0]
            gene_info = gene_info_by_acc.get(base_protein_id, {})
            gene_name = gene_info.get('id', 'Unknown')
            if gene_name is None:
                gene_name = "None"

            gene_ids.add(gene_name)
            clean_proteins.append(protein_id)
        
        genes = ';'.join(sorted(gene_ids))
        return pd.Series([genes, ';'.join(clean_proteins)])

    
    @staticmethod
    def filter_screens(df, screens):
        if isinstance(screens, str):
            return df.loc[df["screen"] == screens]
        elif isinstance(screens, list(str)):
            return df.loc[df["screen"].isin(screens)]
        else:
            raise TypeError("Provides screen(s) as string or list of strings.")