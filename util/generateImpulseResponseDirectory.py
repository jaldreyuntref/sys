def generateImpulseResponseDirectory(script_dir, impulseResponseName):
    newFolderPath = script_dir / impulseResponseName
    newFolderPath.mkdir(parents=True, exist_ok=True)

    filteredImpulseResponsesPath = script_dir / impulseResponseName / "filtered-ir"
    filteredImpulseResponsesPath.mkdir(parents=True, exist_ok=True)

    graphedImpulseResponsesPath = script_dir / impulseResponseName / "graphs"
    graphedImpulseResponsesPath.mkdir(parents=True, exist_ok=True)

    acousticParametersTextFilePath = newFolderPath / "acoustic-parameters.txt"
    acousticParametersTextFilePath.touch(exist_ok=True)

    return acousticParametersTextFilePath