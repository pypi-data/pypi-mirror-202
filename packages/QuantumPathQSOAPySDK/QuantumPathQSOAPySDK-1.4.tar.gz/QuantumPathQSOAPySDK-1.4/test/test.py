from QuantumPathQSOAPySDK import QSOAPlatform
qsoa = QSOAPlatform(configFile=True)

circuit = qsoa.CircuitGates()

# print(circuit.getNumberOfQubits())
# print(circuit.getQubitStates())

circuit.x(3)

# print(circuit.getQubitStates())

# circuit.setDefaultQubitState('-i')

# circuit.x(7)

# print(circuit.getNumberOfQubits())
# print(circuit.getQubitStates())

# circuit.initializeQubitStates(['1', '1', '1', '1'])

print(circuit.getQubitStates())
circuit.setDefaultQubitState('-i')
circuit.x(5)

print(circuit.getParsedBody())