
import pandas as pd
import numpy as np
from dataclasses import dataclass
from tqdm import tqdm

from .process_utils import *
from .data_container import *

@dataclass
class ProteinProcessor(ProcessUtils):
    

    def __post_init__(self):
        super().__post_init__()

    def process_and_normalize(self,
                              data_container,
                              keep_filenames=True,
                              normalize_abundance=False):
        # If normalize_abundance is true, then we'll median normalize,
        # add back in the median for the screen (as proxy for cell type) and 
        # then convert back to linear scale. Otherwise we'll just median 
        # normalized everything by batch so all medians will be 0 and everything 
        # remains log scale.
        if data_container.datatype == "peptide":
            raise ValueError("Function received peptide data. \
                Supply a protein DataContainer or use PeptideProcessor.")
        
        # Melt df so that columns are ["Protein.Ids", "Genes", "Compound",
        # "Abundance", and "batch"]
        melt_df = self._melt_df(data_container.raw_df)
        melt_df = self._get_batch_compound_names(melt_df,
                                                 keep_filenames=keep_filenames)

        if self.label_tfs: # Add column "Is TF" with bools
            melt_df = self._label_tfs(melt_df)

        # Normalize
        if normalize_abundance:
            normalized = self._normalize_abundance(melt_df)
        else:
            normalized = self._median_normalize(melt_df)
            if self.label_screens:
                normalized = self._split_batch_screen(normalized)

        # Drop rows where abundance is nan and put in data_container
        data_container.normalized_df = normalized.loc \
            [normalized["Abundance"].notna()]

    def _normalize_abundance(self, melt_df):
        # Get the median (log) abundances
        overall_median = melt_df["Abundance"].median()
        
        # Median normalize per usual and separate batch and screen into columns
        normalized = self._median_normalize(melt_df)
        normalized = self._split_batch_screen(normalized)

        # Add back the overall median
        normalized["Abundance"] = normalized["Abundance"] + overall_median
        
        # Go back to linear scale
        normalized["Abundance"] = np.exp(normalized["Abundance"])

        return normalized

        
    def _melt_df(self, prot_df):

        quant_cols = [col for col in prot_df.columns \
                      if (col.endswith(".d") or col.endswith(".mzML"))]

        # Log transform 
        quant_pep_df = prot_df.replace({None: np.nan,
                                        0: np.nan}).infer_objects(copy=False)
        quant_pep_df[quant_cols] = np.log(quant_pep_df[quant_cols] \
                                          .astype(float))

        df = quant_pep_df[["Protein.Ids", "Genes"] + quant_cols]
        df = self._drop_nan_cols(df)
        if df.empty:
            raise Exception("Dataframe is empty after dropping NaNs. \
                            Try lowering dropna_percent_threshold.")
        melt_df = df.melt(id_vars=["Protein.Ids", "Genes"],
                          var_name="Compound",
                          value_name="Abundance")
        melt_df = melt_df.loc[melt_df["Abundance"].notna()]
        return melt_df

    def _median_normalize(self, melt_df):
        def subtract_median(group):
            # For a protein in a batch, subtractract the median abundance
            group["Abundance"] = group["Abundance"] - \
                group["Abundance"].median()
            return group
        normalized_df = melt_df.groupby(["Genes", "batch"], observed=False) \
            .apply(subtract_median, include_groups=False).reset_index()
        dropcol = [col for col in normalized_df.columns \
                   if col.startswith("level")][0]
        normalized_df = normalized_df.drop(columns=dropcol)
        return normalized_df