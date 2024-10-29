import os
import tempfile
import zipfile
import koolstof as ks
import pandas as pd
import numpy as np


def _get_samples(sample):
    # Used in get_samples_from_measurements()
    return pd.Series(
        {
            "sample_name": sample.sample_name.iloc[0],
            "salinity": sample.salinity.mean(),
            "temperature": sample.temperature.mean(),
            "pH": sample.pH.mean(),
            "pH_std": sample.pH[sample.pH_good].std(),
            "pH_count": sample.pH.size,
            "pH_good": sample.pH_good.sum(),
            "is_tris": sample.is_tris.all(),
            "extra_mcp": sample.extra_mcp.all(),
        }
    )


def get_xpos(measurements, samples):
    measurements["xpos"] = measurements.order_analysis.astype(float)
    for s, sample in samples.iterrows():
        M = measurements.order_analysis == s
        measurements.loc[M, "xpos"] += (
            0.5 + np.arange(sample.pH_count) - sample.pH_count / 2
        ) * 0.05


def get_samples_from_measurements(measurements):
    # Get one-per-sample table and repopulate xpos column in measurements
    samples = measurements.groupby("order_analysis").apply(
        _get_samples, include_groups=False
    )
    get_xpos(measurements, samples)
    T = samples.is_tris
    samples["pH_tris_expected"] = ks.pH_tris_DD98(
        temperature=samples[T].temperature,
        salinity=samples[T].salinity,
    )
    return samples


def read_agilent(filename):
    measurements = ks.spectro.read_agilent_pH(filename)
    measurements["order_analysis"] = (
        measurements.sample_name.shift() != measurements.sample_name
    ).cumsum()
    measurements["pH_good"] = True
    sns = measurements.sample_name.str.upper().str
    measurements["is_tris"] = sns.startswith("TRIS") | sns.startswith("NT")
    measurements["extra_mcp"] = sns.endswith("-+20")
    return measurements


def read_measurements_create_samples(filename):
    if filename.lower().endswith(".txt"):
        measurements = read_agilent(filename)
    elif filename.lower().endswith(".phroc"):
        measurements = read_phroc(filename)
    elif filename.lower().endswith(".xlsx"):
        measurements = read_excel(filename)
    else:
        print("File type not recognised!")
    # Import pH measurements file and recalculate pH
    measurements["pH"] = ks.spectro.pH_NIOZ(
        measurements.abs578,
        measurements.abs434,
        measurements.abs730,
        temperature=measurements.temperature,
        salinity=measurements.salinity,
    )
    # Create samples table - also repopulates xpos column in measurements
    samples = get_samples_from_measurements(measurements)
    return measurements, samples


def write_phroc(filename, measurements, samples):
    # filename needs to include the **absolute** path to the .phroc file to be saved!
    # Using a relative path will mean it gets saved in the TemporaryDirectory instead
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tdir:
        os.chdir(tdir)
        measurements.to_parquet("measurements.parquet")
        samples.to_parquet("samples.parquet")
        if not filename.endswith(".phroc"):
            filename += ".phroc"
        with zipfile.ZipFile(filename, compression=zipfile.ZIP_LZMA, mode="w") as z:
            z.write("measurements.parquet")
            z.write("samples.parquet")
    os.chdir(cwd)


def write_excel(filename, measurements, samples):
    if not filename.endswith(".xlsx"):
        filename += ".xlsx"
    with pd.ExcelWriter(filename, engine="openpyxl") as w:
        samples.to_excel(w, sheet_name="Samples")
        measurements.to_excel(w, sheet_name="Measurements")


def read_phroc(filename):
    with tempfile.TemporaryDirectory() as tdir:
        with zipfile.ZipFile(filename, "r") as z:
            z.extractall(tdir)
        measurements = pd.read_parquet(os.path.join(tdir, "measurements.parquet"))
        samples = pd.read_parquet(os.path.join(tdir, "samples.parquet"))
    return measurements, samples


def read_excel(filename):
    measurements = pd.read_excel(filename, sheet_name="Measurements").set_index("order")
    samples = pd.read_excel(filename, sheet_name="Samples").set_index("order_analysis")
    return measurements, samples
