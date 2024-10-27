
__version__ = "0.1"


from .data_processing import prepare_data
from .training import train , predict , evaluate
from .visualization import visualize


# Sabitleri tanımla
DEFAULT_SEED = 42

# Başlatma fonksiyonu
def init():
    print(f"mkyz package initialized. Version: {__version__}")

# Başlatma işlemini gerçekleştir
init()
