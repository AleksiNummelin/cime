# Utility functions used in system_test.py
from XML.standard_module_setup import *
from CIME.XML.testlist import Testlist
from CIME.XML.files import Files
import CIME.utils
logger = logging.getLogger(__name__)

def get_tests_from_xml(xml_machine=None,xml_category=None,xml_compiler=None, xml_testlist=None,
                       machine=None, compiler=None):
    """
    Parse testlists for a list of tests
    """
    listoftests = []
    testlistfiles = []
    if(machine is not None):
        thismach=machine
    if(compiler is not None):
        thiscompiler = compiler

    if(xml_testlist is not None):
        expect(os.path.isfile(xml_testlist), "Testlist not found or not readable "+xml_testlist)
        testlistfiles.append(xml_testlist)
    else:
        files = Files()
        test_spec_files = files.get_values("TESTS_SPEC_FILE","component")
        for spec_file in test_spec_files.viewvalues():
            if(os.path.isfile(spec_file)):
                testlistfiles.append(spec_file)

    for testlistfile in testlistfiles:
        thistestlistfile = Testlist(testlistfile)
        logger.debug("Testlist file is "+testlistfile)
        logger.debug("xml_machine %s xml_category %s xml_compiler %s"%(xml_machine, xml_category, xml_compiler))
        newtests =  thistestlistfile.get_tests(xml_machine, xml_category, xml_compiler)
        for test in newtests:
            if(machine is None):
                thismach = test["machine"]
            if(compiler is None):
                thiscompiler = test["compiler"]
            test["name"] = CIME.utils.get_full_test_name(test["testname"], test["grid"], test["compset"], thismach, thiscompiler,
                                                         None if "testmods" not in test else test["testmods"])
            logger.debug("Adding test "+test["name"])
        listoftests += newtests
        logger.info("Found %d tests"% len(listoftests))

    return listoftests
