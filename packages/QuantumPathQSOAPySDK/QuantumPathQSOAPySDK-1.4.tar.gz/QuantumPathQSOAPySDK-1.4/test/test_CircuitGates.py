import unittest
from QuantumPathQSOAPySDK import QSOAPlatform

##################_____GET CIRCUIT BODY_____##################
class Test_GetCircuitBody(unittest.TestCase):

    # GET CIRCUIT BODY EMPTY
    def test_getCircuitBody_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuitBody = circuit.getCircuitBody()

        self.assertEqual(circuitBody, [[]]) # check circuit body
    
    # GET CIRCUIT BODY WITH GATES
    def test_getCircuitBody_gates(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        circuitBody = circuit.getCircuitBody()

        self.assertEqual(circuitBody, [['H']]) # check circuit body


##################_____GET QUBIT STATES_____##################
class Test_GetQubitStates(unittest.TestCase):

    # GET QUBIT STATES EMPTY
    def test_getQubitStates_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        qubitStates = circuit.getQubitStates()

        self.assertEqual(qubitStates, []) # check qubit states
    
    # GET QUBIT STATES
    def test_getQubitStates(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(2)

        qubitStates = circuit.getQubitStates()

        self.assertEqual(qubitStates, ['0', '0', '0']) # check qubit states


##################_____GET PARSED BODY_____##################
class Test_GetParsedBody(unittest.TestCase):

    # GET PARSED BODY EMPTY
    def test_getParsedBody_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        parsedBody = circuit.getParsedBody()

        self.assertEqual(parsedBody, 'circuit={"cols":[[]], "init":[]}') # check circuit body
    
    # GET PARSED BODY WITH GATES
    def test_getParsedBody_gates(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        circuitBody = circuit.getParsedBody()

        self.assertEqual(circuitBody, 'circuit={"cols":[["H"]], "init":["0"]}') # check circuit body


##################_____GET NUMBER OF QUBITS_____##################
class Test_GetNumberOfQubits(unittest.TestCase):

    # GET NUMBER OF QUBITS EMPTY
    def test_getNumberOfQubits_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        numberOfQubits = circuit.getNumberOfQubits()

        self.assertEqual(numberOfQubits, 0) # check number of qubits
    
    # GET NUMBER OF QUBITS
    def test_getNumberOfQubits(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(2)

        numberOfQubits = circuit.getNumberOfQubits()

        self.assertEqual(numberOfQubits, 3) # check number of qubits


##################_____GET DEFAULT QUBIT STATE_____##################
class Test_GetDefaultQubitState(unittest.TestCase):

    # GET DEFAULT QUBIT STATE
    def test_getDefaultQubitState(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        defaultQubitState = circuit.getDefaultQubitState()

        self.assertEqual(defaultQubitState, '0') # check default qubit state


##################_____SET DEFAULT QUBIT STATE_____##################
class Test_SetDefaultQubitState(unittest.TestCase):

    # SET DEFAULT QUBIT STATE
    def test_setDefaultQubitState(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.setDefaultQubitState('1')

        defaultQubitState = circuit.getDefaultQubitState()

        self.assertEqual(defaultQubitState, '1') # check default qubit state

    # SET DEFAULT STATE EXISTING CIRCUIT
    def test_setDefaultQubitState_existingCircuit(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)
        circuit.setDefaultQubitState('1')
        circuit.h(2)

        qubitStates = circuit.getQubitStates()

        self.assertEqual(qubitStates, ['0', '1', '1']) # check qubit states
    
    # BAD ARGUMENT qubitState
    def test_setDefaultQubitState_badArgument_qubitState(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.setDefaultQubitState('state')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')
    
    # BAD ARGUMENT TYPE qubitState
    def test_setDefaultQubitState_badArgumentType_qubitState(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.setDefaultQubitState(0)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____GET PARSED BODY_____##################
class Test_GetNumberOfQubits(unittest.TestCase):

    # GET PARSED BODY EMPTY
    def test_getParsedBody_empty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        parsedBody = circuit.getParsedBody()

        self.assertEqual(parsedBody, 'circuit={"cols":[[]]}') # check parsed circuit body
    
    # GET PARSED BODY
    def test_getParsedBody(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        parsedBody = circuit.getParsedBody()

        self.assertEqual(parsedBody, 'circuit={"cols":[["H"]]}') # check parsed circuit body


##################_____INITIALIZE QUBIT STATES_____##################
class Test_InitializeQubitStates(unittest.TestCase):

    # INITIALIZE QUBIT STATES
    def test_initializeQubitStates(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(2)

        circuit.initializeQubitStates(['1', '1', '1'])

        qubitStates = circuit.getQubitStates()

        self.assertEqual(qubitStates, ['1', '1', '1']) # check qubit states

    # BAD ARGUMENT qubitStates
    def test_initializeQubitStates_badArgument_qubitStates(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.initializeQubitStates(['1', '1', '1'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT qubitStates LIST
    def test_initializeQubitStates_badArgument_qubitStates_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.initializeQubitStates(['1', '1', 'state'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'ValueError')

    # BAD ARGUMENT TYPE qubitStates
    def test_initializeQubitStates_badArgumentType_qubitStates(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.initializeQubitStates('states')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE qubitStates LIST
    def test_initializeQubitStates_badArgumentType_qubitStates_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(2)

        try:
            circuit.initializeQubitStates(['1', '1', 1])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____H_____##################
class Test_H(unittest.TestCase):

    # H
    def test_h(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.h(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'H']]) # check circuit body

    # H LIST
    def test_h_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(1)

        circuit.h([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['H', 'X', 'H'], [1, 'H']]) # check circuit body
    
    # H ALL
    def test_h_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(1)

        circuit.h()

        self.assertEqual(circuit.getCircuitBody(), [['H', 'X'], [1, 'H']]) # check circuit body

    # H ADD FALSE
    def test_h_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.h(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_h_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.h('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_h_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.h([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_h_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.h(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____X_____##################
class Test_X(unittest.TestCase):

    # X
    def test_x(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.x(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'X']]) # check circuit body

    # X LIST
    def test_x_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.x([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['X', 'H', 'X'], [1, 'X']]) # check circuit body
    
    # X ALL
    def test_x_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.x()

        self.assertEqual(circuit.getCircuitBody(), [['X', 'H'], [1, 'X']]) # check circuit body

    # X ADD FALSE
    def test_x_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.x(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_x_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.x('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_x_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.x([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_x_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.x(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____Y_____##################
class Test_Y(unittest.TestCase):

    # Y
    def test_y(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.y(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'Y']]) # check circuit body

    # Y LIST
    def test_y_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.y([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['Y', 'H', 'Y'], [1, 'Y']]) # check circuit body
    
    # Y ALL
    def test_y_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.y()

        self.assertEqual(circuit.getCircuitBody(), [['Y', 'H'], [1, 'Y']]) # check circuit body

    # Y ADD FALSE
    def test_y_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.y(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_y_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.y('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_y_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.y([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_y_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.y(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____Z_____##################
class Test_Z(unittest.TestCase):

    # Z
    def test_z(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.z(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'Z']]) # check circuit body

    # Z LIST
    def test_z_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.z([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['Z', 'H', 'Z'], [1, 'Z']]) # check circuit body
    
    # Z ALL
    def test_z_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.z()

        self.assertEqual(circuit.getCircuitBody(), [['Z', 'H'], [1, 'Z']]) # check circuit body

    # Z ADD FALSE
    def test_z_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.z(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_z_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.z('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_z_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.z([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_z_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.z(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____S_____##################
class Test_S(unittest.TestCase):

    # S
    def test_s(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.s(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'S']]) # check circuit body

    # S LIST
    def test_s_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.s([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['S', 'H', 'S'], [1, 'S']]) # check circuit body
    
    # S ALL
    def test_s_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.s()

        self.assertEqual(circuit.getCircuitBody(), [['S', 'H'], [1, 'S']]) # check circuit body

    # S ADD FALSE
    def test_s_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.s(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_s_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.s('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_s_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.s([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_s_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.s(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____I_S_____##################
class Test_I_S(unittest.TestCase):

    # I_S
    def test_i_s(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.i_s(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_S']]) # check circuit body

    # I_S LIST
    def test_i_s_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.i_s([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['I_S', 'H', 'I_S'], [1, 'I_S']]) # check circuit body
    
    # I_S ALL
    def test_i_s_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.i_s()

        self.assertEqual(circuit.getCircuitBody(), [['I_S', 'H'], [1, 'I_S']]) # check circuit body

    # I_S ADD FALSE
    def test_i_s_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.i_s(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_i_s_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_s('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_i_s_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_s([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_i_s_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_s(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____SX_____##################
class Test_SX(unittest.TestCase):

    # SX
    def test_sx(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.sx(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'SX']]) # check circuit body

    # SX LIST
    def test_sx_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.sx([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['SX', 'H', 'SX'], [1, 'SX']]) # check circuit body
    
    # SX ALL
    def test_sx_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.sx()

        self.assertEqual(circuit.getCircuitBody(), [['SX', 'H'], [1, 'SX']]) # check circuit body

    # SX ADD FALSE
    def test_sx_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.sx(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_sx_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sx('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_sx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_sx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sx(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____I_SX_____##################
class Test_I_SX(unittest.TestCase):

    # I_SX
    def test_i_sx(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.i_sx(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_SX']]) # check circuit body

    # I_SX LIST
    def test_i_sx_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.i_sx([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['I_SX', 'H', 'I_SX'], [1, 'I_SX']]) # check circuit body
    
    # I_SX ALL
    def test_i_sx_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.i_sx()

        self.assertEqual(circuit.getCircuitBody(), [['I_SX', 'H'], [1, 'I_SX']]) # check circuit body

    # I_SX ADD FALSE
    def test_i_sx_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.i_sx(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_i_sx_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sx('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_i_sx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_i_sx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sx(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____SY_____##################
class Test_SY(unittest.TestCase):

    # SY
    def test_sy(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.sy(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'SY']]) # check circuit body

    # SY LIST
    def test_sy_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.sy([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['SY', 'H', 'SY'], [1, 'SY']]) # check circuit body
    
    # SY ALL
    def test_sy_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.sy()

        self.assertEqual(circuit.getCircuitBody(), [['SY', 'H'], [1, 'SY']]) # check circuit body

    # SY ADD FALSE
    def test_sy_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.sy(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_sy_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sy('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_sy_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sy([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_sy_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sy(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____I_SY_____##################
class Test_I_SY(unittest.TestCase):

    # I_SY
    def test_i_sy(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.i_sy(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_SY']]) # check circuit body

    # I_SY LIST
    def test_i_sy_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.i_sy([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['I_SY', 'H', 'I_SY'], [1, 'I_SY']]) # check circuit body
    
    # I_SY ALL
    def test_i_sy_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.i_sy()

        self.assertEqual(circuit.getCircuitBody(), [['I_SY', 'H'], [1, 'I_SY']]) # check circuit body

    # I_SY ADD FALSE
    def test_i_sy_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.i_sy(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_i_sy_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sy('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_i_sy_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sy([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_i_sy_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sy(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____T_____##################
class Test_T(unittest.TestCase):

    # T
    def test_t(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.t(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'T']]) # check circuit body

    # T LIST
    def test_t_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.t([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['T', 'H', 'T'], [1, 'T']]) # check circuit body
    
    # T ALL
    def test_t_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.t()

        self.assertEqual(circuit.getCircuitBody(), [['T', 'H'], [1, 'T']]) # check circuit body

    # T ADD FALSE
    def test_t_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.t(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_t_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.t('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_t_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.t([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_t_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.t(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____I_T_____##################
class Test_I_T(unittest.TestCase):

    # I_T
    def test_i_t(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.i_t(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_T']]) # check circuit body

    # I_T LIST
    def test_i_t_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.i_t([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['I_T', 'H', 'I_T'], [1, 'I_T']]) # check circuit body
    
    # I_T ALL
    def test_i_t_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.i_t()

        self.assertEqual(circuit.getCircuitBody(), [['I_T', 'H'], [1, 'I_T']]) # check circuit body

    # I_T ADD FALSE
    def test_i_t_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.i_t(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_i_t_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_t('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_i_t_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_t([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_i_t_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_t(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____TX_____##################
class Test_TX(unittest.TestCase):

    # TX
    def test_tx(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.tx(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'TX']]) # check circuit body

    # TX LIST
    def test_tx_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.tx([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['TX', 'H', 'TX'], [1, 'TX']]) # check circuit body
    
    # TX ALL
    def test_tx_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.tx()

        self.assertEqual(circuit.getCircuitBody(), [['TX', 'H'], [1, 'TX']]) # check circuit body

    # TX ADD FALSE
    def test_tx_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.tx(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_tx_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.tx('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_tx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.tx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_tx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.tx(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____I_TX_____##################
class Test_I_TX(unittest.TestCase):

    # I_TX
    def test_i_tx(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.i_tx(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_TX']]) # check circuit body

    # I_TX LIST
    def test_i_tx_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.i_tx([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['I_TX', 'H', 'I_TX'], [1, 'I_TX']]) # check circuit body
    
    # I_TX ALL
    def test_i_tx_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.i_tx()

        self.assertEqual(circuit.getCircuitBody(), [['I_TX', 'H'], [1, 'I_TX']]) # check circuit body

    # I_TX ADD FALSE
    def test_i_tx_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.i_tx(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_i_tx_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_tx('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_i_tx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_tx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_i_tx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_tx(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____TY_____##################
class Test_TY(unittest.TestCase):

    # TY
    def test_ty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.ty(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'TY']]) # check circuit body

    # TY LIST
    def test_ty_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.ty([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['TY', 'H', 'TY'], [1, 'TY']]) # check circuit body
    
    # TY ALL
    def test_ty_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.ty()

        self.assertEqual(circuit.getCircuitBody(), [['TY', 'H'], [1, 'TY']]) # check circuit body

    # TY ADD FALSE
    def test_ty_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.ty(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_ty_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ty('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_ty_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ty([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_ty_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ty(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____I_TY_____##################
class Test_I_TY(unittest.TestCase):

    # I_TY
    def test_i_ty(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.i_ty(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_TY']]) # check circuit body

    # I_TY LIST
    def test_i_ty_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.i_ty([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['I_TY', 'H', 'I_TY'], [1, 'I_TY']]) # check circuit body
    
    # I_TY ALL
    def test_i_ty_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.i_ty()

        self.assertEqual(circuit.getCircuitBody(), [['I_TY', 'H'], [1, 'I_TY']]) # check circuit body

    # I_TY ADD FALSE
    def test_i_ty_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.i_ty(0, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_i_ty_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_ty('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_i_ty_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_ty([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_i_ty_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_ty(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____P_____##################
class Test_P(unittest.TestCase):

    # P
    def test_p(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.p(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, {'arg': 'pi', 'id': 'P'}]]) # check circuit body

    # P ARGUMENT INT
    def test_p_argument_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.p(1, 2)

        self.assertEqual(circuit.getCircuitBody(), [[1, {'arg': '2', 'id': 'P'}]]) # check circuit body

    # P ARGUMENT STR
    def test_p_argument_str(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.p(1, 'pi/2')

        self.assertEqual(circuit.getCircuitBody(), [[1, {'arg': 'pi/2', 'id': 'P'}]]) # check circuit body

    # P LIST
    def test_p_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.p([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'P'}, 'H', {'arg': 'pi', 'id': 'P'}], [1, {'arg': 'pi', 'id': 'P'}]]) # check circuit body
    
    # P ALL
    def test_p_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.p()

        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'P'}, 'H'], [1, {'arg': 'pi', 'id': 'P'}]]) # check circuit body

    # P ADD FALSE
    def test_p_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.p(0, add=False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_p_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.p('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_p_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.p([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE argument
    def test_p_badArgumentType_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.p(0, True)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_p_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.p(0, add='add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____RX_____##################
class Test_RX(unittest.TestCase):

    # RX
    def test_rx(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.rx(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, {'arg': 'pi', 'id': 'RX'}]]) # check circuit body

    # RX ARGUMENT INT
    def test_rx_argument_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.rx(1, 2)

        self.assertEqual(circuit.getCircuitBody(), [[1, {'arg': '2', 'id': 'RX'}]]) # check circuit body

    # RX ARGUMENT STR
    def test_rx_argument_str(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.rx(1, 'pi/2')

        self.assertEqual(circuit.getCircuitBody(), [[1, {'arg': 'pi/2', 'id': 'RX'}]]) # check circuit body

    # RX LIST
    def test_rx_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.rx([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'RX'}, 'H', {'arg': 'pi', 'id': 'RX'}], [1, {'arg': 'pi', 'id': 'RX'}]]) # check circuit body
    
    # RX ALL
    def test_rx_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.rx()

        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'RX'}, 'H'], [1, {'arg': 'pi', 'id': 'RX'}]]) # check circuit body

    # RX ADD FALSE
    def test_rx_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.rx(0, add=False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_rx_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_rx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE argument
    def test_rx_badArgumentType_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx(0, True)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_rx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx(0, add='add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____RY_____##################
class Test_RY(unittest.TestCase):

    # RY
    def test_ry(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.ry(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, {'arg': 'pi', 'id': 'RY'}]]) # check circuit body

    # RY ARGUMENT INT
    def test_ry_argument_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.ry(1, 2)

        self.assertEqual(circuit.getCircuitBody(), [[1, {'arg': '2', 'id': 'RY'}]]) # check circuit body

    # RY ARGUMENT STR
    def test_ry_argument_str(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.ry(1, 'pi/2')

        self.assertEqual(circuit.getCircuitBody(), [[1, {'arg': 'pi/2', 'id': 'RY'}]]) # check circuit body

    # RY LIST
    def test_ry_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.ry([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'RY'}, 'H', {'arg': 'pi', 'id': 'RY'}], [1, {'arg': 'pi', 'id': 'RY'}]]) # check circuit body
    
    # RY ALL
    def test_ry_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.ry()

        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'RY'}, 'H'], [1, {'arg': 'pi', 'id': 'RY'}]]) # check circuit body

    # RY ADD FALSE
    def test_ry_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.ry(0, add=False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_ry_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_ry_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE argument
    def test_ry_badArgumentType_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry(0, True)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_ry_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry(0, add='add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____RZ_____##################
class Test_RZ(unittest.TestCase):

    # RZ
    def test_rz(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.rz(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, {'arg': 'pi', 'id': 'RZ'}]]) # check circuit body

    # RZ ARGUMENT INT
    def test_rz_argument_int(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.rz(1, 2)

        self.assertEqual(circuit.getCircuitBody(), [[1, {'arg': '2', 'id': 'RZ'}]]) # check circuit body

    # RZ ARGUMENT STR
    def test_rz_argument_str(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.rz(1, 'pi/2')

        self.assertEqual(circuit.getCircuitBody(), [[1, {'arg': 'pi/2', 'id': 'RZ'}]]) # check circuit body

    # RZ LIST
    def test_rz_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.rz([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'RZ'}, 'H', {'arg': 'pi', 'id': 'RZ'}], [1, {'arg': 'pi', 'id': 'RZ'}]]) # check circuit body
    
    # RZ ALL
    def test_rz_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.rz()

        self.assertEqual(circuit.getCircuitBody(), [[{'arg': 'pi', 'id': 'RZ'}, 'H'], [1, {'arg': 'pi', 'id': 'RZ'}]]) # check circuit body

    # RZ ADD FALSE
    def test_rz_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.rz(0, add=False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_rz_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_rz_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE argument
    def test_rz_badArgumentType_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz(0, True)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_rz_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz(0, add='add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____SWAP_____##################
class Test_Swap(unittest.TestCase):

    # SWAP
    def test_swap(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        circuit.swap(1, 3)

        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'Swap', 1, 'Swap']]) # check circuit body

    # SWAP ADD FALSE
    def test_swap_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.swap(1, 3, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position1
    def test_swap_badArgumentType_position1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.swap('position', 3)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position2
    def test_swap_badArgumentType_position2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.swap(1, 'position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_swap_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.swap(1, 3, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____CH_____##################
class Test_CH(unittest.TestCase):

    # CH
    def test_ch(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        circuit.ch(1, 3)

        self.assertEqual(circuit.getCircuitBody(), [['X'], [1, 'CTRL', 1, 'H']]) # check circuit body

    # CH ADD FALSE
    def test_ch_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.ch(1, 3, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position1
    def test_ch_badArgumentType_position1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ch('position', 3)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position2
    def test_ch_badArgumentType_position2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ch(1, 'position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_ch_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ch(1, 3, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____CX_____##################
class Test_CX(unittest.TestCase):

    # CX
    def test_cx(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        circuit.cx(1, 3)

        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 1, 'X']]) # check circuit body

    # CX ADD FALSE
    def test_cx_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.cx(1, 3, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position1
    def test_cx_badArgumentType_position1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.cx('position', 3)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position2
    def test_cx_badArgumentType_position2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.cx(1, 'position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_cx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.cx(1, 3, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____CCX_____##################
class Test_CCX(unittest.TestCase):

    # CCX
    def test_ccx(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        circuit.ccx(1, 2, 3)

        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'CTRL', 'X']]) # check circuit body

    # CCX ADD FALSE
    def test_ccx_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.ccx(1, 2, 3, False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT TYPE position1
    def test_ccx_badArgumentType_position1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx('position', 2, 3)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position2
    def test_ccx_badArgumentType_position2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx(1, 'position', 3)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position3
    def test_ccx_badArgumentType_position3(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx(1, 2, 'position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_ccx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx(1, 2, 3, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____MEASURE_____##################
class Test_Measure(unittest.TestCase):

    # MEASURE
    def test_measure(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.measure(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'Measure']]) # check circuit body

    # MEASURE LIST
    def test_measure_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.measure([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['Measure', 'Measure', 'Measure']]) # check circuit body
    
    # MEASURE ALL
    def test_measure_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.measure()

        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['Measure', 'Measure']]) # check circuit body
    
    # BAD ARGUMENT TYPE position LIST
    def test_measure_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.measure([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____BARRIER_____##################
class Test_Barrier(unittest.TestCase):

    # BARRIER
    def test_barrier(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.barrier(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'SPACER']]) # check circuit body

    # BARRIER LIST
    def test_barrier_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.barrier([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [['SPACER', 'H', 'SPACER'], [1, 'SPACER']]) # check circuit body
    
    # BARRIER ALL
    def test_barrier_all(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.barrier()

        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['SPACER', 'SPACER']]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_barrier_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier('position')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_barrier_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_barrier_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier(0, 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____BEGIN REPEAT_____##################
class Test_BeginRepeat(unittest.TestCase):

    # BEGIN REPEAT
    def test_beginRepeat(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.beginRepeat(1, 2)

        self.assertEqual(circuit.getCircuitBody(), [[1, {'arg': '2', 'id': 'BEGIN_R'}]]) # check circuit body

    # BEGIN REPEAT LIST
    def test_beginRepeat_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.beginRepeat([0, 1], 2)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], [{'arg': '2', 'id': 'BEGIN_R'}, {'arg': '2', 'id': 'BEGIN_R'}]]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_beginRepeat_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat('position', 2)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_beginRepeat_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat([0, 'position'], 2)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE repetitions
    def test_beginRepeat_badArgumentType_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat(0, 'repetitions')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____END REPEAT_____##################
class Test_EndRepeat(unittest.TestCase):

    # END REPEAT
    def test_endRepeat(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.endRepeat(1)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'END_R']]) # check circuit body

    # END REPEAT LIST
    def test_endRepeat_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.endRepeat([0, 1, 2])

        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['END_R', 'END_R', 'END_R']]) # check circuit body

    # BAD ARGUMENT TYPE position LIST
    def test_endRepeat_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.endRepeat([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____CONTROL_____##################
class Test_Control(unittest.TestCase):

    # CONTROL
    def test_control(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        cx = circuit.control(1, circuit.x(2, False))
        circuit.addCreatedGate(cx)

        self.assertEqual(circuit.getCircuitBody(), [[1, 'CTRL', 'X']]) # check circuit body
    
    # BAD ARGUMENT circuit
    def test_control_badArgument_circuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        cx = circuit.control(1, circuit.x(2))
        circuit.addCreatedGate(cx)

        self.assertNotEqual(circuit.getCircuitBody(), [[1, 'CTRL', 'X']]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_control_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            cx = circuit.control('position', circuit.h(2, False))
            circuit.addCreatedGate(cx)
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE circuit
    def test_control_badArgumentType_circuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.control(1, 'circuit')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____ADD CREATED GATE_____##################
class Test_AddCreatedGate(unittest.TestCase):

    # ADD CREATED GATE
    def test_addCreatedGate(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        cx = circuit.control(0, circuit.x(1, False))
        circuit.addCreatedGate(cx)

        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'X']]) # check circuit body

    # BAD ARGUMENT TYPE gate
    def test_addCreatedGate_badArgumentType_gate(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.addCreatedGate('gate')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')


##################_____MULTI CONTROL GATE_____##################
class Test_MCG(unittest.TestCase):

    # MCG
    def test_mcg(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.mcg(1, circuit.x(3, False))

        self.assertEqual(circuit.getCircuitBody(), [[1, 'CTRL', 1, 'X']]) # check circuit body

    # MCG LIST
    def test_mcg_list(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        circuit.mcg([0, 2], circuit.x(3, False))

        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['CTRL', 1, 'CTRL', 'X']]) # check circuit body

    # MCG ADD FALSE
    def test_mcg_addFalse(self):
        qsoa = QSOAPlatform()
        circuit = qsoa.CircuitGates()

        circuit.mcg([0, 2], circuit.x(3, False), False)

        self.assertEqual(circuit.getCircuitBody(), [[]]) # check circuit body

    # BAD ARGUMENT circuit
    def test_mcg_badArgument_circuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        circuit.mcg(1, circuit.x(3))

        self.assertNotEqual(circuit.getCircuitBody(), [[1, 'CTRL', 1, 'X']]) # check circuit body

    # BAD ARGUMENT TYPE position
    def test_mcg_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg('position', circuit.x(3, False))
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE position LIST
    def test_mcg_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([0, 'position'], circuit.x(3, False))
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

    # BAD ARGUMENT TYPE add
    def test_mcg_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([0, 2], circuit.x(3, False), 'add')
            raise Exception

        except Exception as e:
            self.assertEqual(type(e).__name__, 'TypeError')

if __name__ == '__main__':
    unittest.main()