import sys 
sys.path.append('.')

from pathlib import Path
from corems.transient.input.brukerSolarix import ReadBrukerSolarix
from corems.mass_spectrum.calc.MassErrorPrediction import MassErrorPrediction
from corems.molecular_id.search.molecularFormulaSearch import SearchMolecularFormulas


def x_test_error_prediction(mass_spectrum_ftms):
    'This function will be removed in CoreMS 2.0. adding x to skip test'
    mass_spectrum = mass_spectrum_ftms

    mass_error_prediction = MassErrorPrediction(mass_spectrum)
    
    mass_error_prediction.get_results()

    return mass_spectrum

if __name__ == "__main__":
    x_test_error_prediction()
