
# Just random code for using JIDT


# jarLocation = "/Users/Sepehr/Documents/Projects/SepehrMN-Github/infodynamics-dist-1.3.1/infodynamics.jar"
# # Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
# jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

# sourceArray = [random.randint(0,1) for r in range(100)]
# destArray = [0] + sourceArray[0:99]
# sourceArray2 = jpype.JArray(jpype.JInt,1)([1,2,2,1,2,1])

# sourceArray = np.asarray([random.randint(0,1) for r in range(100)]).astype("int32")
# destArray = [0] + sourceArray[0:99]
# sourceArray2 = [random.randint(0,1) for r in range(100)]

# Create a TE calculator and run it:
# teCalcClass = jpype.JPackage("infodynamics.measures.discrete").TransferEntropyCalculatorDiscrete
# teCalc = teCalcClass(2,1)
# teCalc.initialise()

# cmiCalcClass = jpype.JPackage("infodynamics.measures.discrete").ConditionalMutualInformationCalculatorDiscrete
# cmiCalc = cmiCalcClass(2, 2, 2) #bases
# cmiCalc.initialise()
# cmiCalc.addObservations(sourceArray, sourceArray, sourceArray)
# cmiCalc.computeAverageLocalOfObservations()




#additive
#r + c

# Modulatory
# 0.5r[1+exp(rc)]

# both
# 0.5r[1+exp(rc)] + c


# Activation function
# y = 1 / 1 + exp(-A)  # y is a probabilistic binary output