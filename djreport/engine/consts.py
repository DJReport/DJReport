# engines
STIMULSOFT = "stimulsoft"
FASTREPORT = "fastreport"

ENGINES = (
    STIMULSOFT,
    FASTREPORT,
)

ENGINE_CHOICES = ((STIMULSOFT, "Stimulsoft"), (FASTREPORT, "FastReport"))


# bins
STIMULSOFT_BIN = "DJREPORT_STIMULSOFT"
FASTREPORT_BIN = "DJREPORT_FASTREPORT"

BINS = {
    STIMULSOFT: STIMULSOFT_BIN,
    FASTREPORT: FASTREPORT_BIN,
}


# dpi
MIN_DPI = 96
MAX_DPI = 300


# formats
CSV = "csv"
DATA = "data"
DBF = "dbf"
DIF = "dif"
EXCEL = "excel"
HTML = "html"
HTML5 = "html5"
PDF = "pdf"
BMP = "bmp"
EMF = "emf"
GIF = "gif"
JPEG = "jpeg"
PCX = "pcx"
PNG = "png"
SVG = "svg"
SVGZ = "svgz"
TIFF = "tiff"
JSON = "json"
MHT = "mht"
ODS = "ods"
ODT = "odt"
POWER_POINT = "powerpoint"
RTF = "rtf"
SYLK = "sylk"
WORD = "word"
XML = "xml"
XPS = "xps"

FORMATS = (
    CSV,
    DATA,
    DBF,
    DIF,
    EXCEL,
    HTML,
    HTML5,
    PDF,
    BMP,
    EMF,
    GIF,
    JPEG,
    PCX,
    PNG,
    SVG,
    SVGZ,
    TIFF,
    JSON,
    MHT,
    ODS,
    ODT,
    POWER_POINT,
    RTF,
    SYLK,
    WORD,
    XML,
    XPS,
)


# extensions
EXTENSIONS = {
    CSV: "csv",
    DATA: "data",
    DBF: "dbf",
    DIF: "dif",
    EXCEL: "xls",
    HTML: "html",
    HTML5: "html",
    PDF: "pdf",
    BMP: "bmp",
    EMF: "emf",
    GIF: "gif",
    JPEG: "jpeg",
    PCX: "pcx",
    PNG: "png",
    SVG: "svg",
    SVGZ: "svgz",
    TIFF: "tiff",
    JSON: "json",
    MHT: "mht",
    ODS: "ods",
    ODT: "odt",
    POWER_POINT: "ppt",
    RTF: "rtf",
    SYLK: "slk",
    WORD: "doc",
    XML: "xml",
    XPS: "xps",
}
