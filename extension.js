const fs = require('fs');
const {readFile, writeFile, promises: fsPromises} = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const vscode = require('vscode');
let outputChannel = vscode.window.createOutputChannel("Smell-Fixer");

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	let quickScan = vscode.commands.registerCommand('extension.quickscan', function () {
	
		let fileName = vscode.window.activeTextEditor.document.fileName;
		let codeLang = vscode.window.activeTextEditor.document.languageId;
		let sourceCode = vscode.window.activeTextEditor.document.getText();
				
		if (codeLang === 'python') {
			if (sourceCode.trim('\n').length !== 0){
				analyzeSourceFile(sourceCode, fileName);
				refactorSourceFile(sourceCode,fileName)

			} else { 
				vscode.window.showErrorMessage("Empty source code!");
			}
		} else {
			vscode.window.showErrorMessage("Please select Python source code!");
		}
	});

	let completeScan = vscode.commands.registerCommand('extension.completescan', function () {

		let workspaceFolder = vscode.workspace.workspaceFolders[0].uri.fsPath;
		let filesInWorkspaceFolder = getAllFiles(workspaceFolder, []);
		filesInWorkspaceFolder.forEach(file => {
			try{
				//if(file.includes(".git") == false && file.includes("test") == false){
		
					file = workspaceFolder+file.split(workspaceFolder)[1];
					//console.log(file)
					if(getFileExtension(file) === 'py'){
						
						let sourceCode = getFileContentsFromPath(file);
						if (sourceCode != null) {
							analyzeSourceFile(sourceCode, file);
						}
					}
				//}
			} catch(error){ vscode.window.showErrorMessage("could not read file - "+ file); }
		});
		refactorFolder(workspaceFolder,filesInWorkspaceFolder)
	});

	let customScan = vscode.commands.registerCommand('extension.customscan', function () {
		
		const userPathInput = vscode.window.showInputBox();
		userPathInput.then( userSpecifiedPath => {
			
			if (checkIfFilePath(userSpecifiedPath)){
				if (getFileExtension(userSpecifiedPath) === 'py') {

					let sourceCode = getFileContentsFromPath(userSpecifiedPath);
					if (sourceCode.trim('\n').length !== 0) {
						analyzeSourceFile(sourceCode, userSpecifiedPath);
						refactorSourceFile(sourceCode,userSpecifiedPath)
					} 
					else vscode.window.showErrorMessage("Empty source code!");
				}
				else vscode.window.showErrorMessage("Please select Python source code!");
			}
			else{
				
				console.log({"specified path ": userSpecifiedPath});
				let allFiles = getAllFiles(userSpecifiedPath, []);

				allFiles.forEach(file => {
				
					try {
						//if(file.includes(".git") == false && file.includes("test") == false){
							file = userSpecifiedPath+file.split(userSpecifiedPath)[1];
							console.log(file);
						
							if(getFileExtension(file) === 'py'){
								
								let sourceCode = getFileContentsFromPath(file);
								console.log("no problem here!");
			
								if (sourceCode != null) {
									analyzeSourceFile(sourceCode, file);
								}
							}
						//}
					} catch(error){ vscode.window.showErrorMessage("could not read file - "+ file);}
				});
				refactorFolder(userSpecifiedPath,allFiles)
			}
		});
	});

	context.subscriptions.push(quickScan);
	context.subscriptions.push(completeScan);
	context.subscriptions.push(customScan);
}

const analyzeSourceFile = (sourceCode, fileName) => {
	var script = spawn('python', [__dirname+"/py-scripts/smellDetect.py",sourceCode,fileName])
	script.stdout.on('data', function(warnings){
		makeWarningsVisibleInNotification(warnings.toString())
	})

};

const refactorSourceFile = (sourceCode, fileName) => {
	vscode.window.showInformationMessage('Do you want to refactor?','Yes','No')
	.then(selection => {
		if(selection === "Yes"){
			const script = spawn('python', [__dirname+"/py-scripts/refactor.py",sourceCode]);
			script.stdout.on('data', function(data){
				writeFile(fileName,data.toString(),'utf-8', function(err){
					console.log("refactor is done")
				})
			})
		}
	})
}

const refactorFolder = (workspaceFolder, fileNameList) =>{
	vscode.window.showInformationMessage('Do you want to refactor?', 'Yes', 'No')
	.then(selection =>{
		if(selection === "Yes"){
			fileNameList.forEach(file =>{
				try{
					//if(file.includes(".git") == false && file.includes("test") == false){
			
						file = workspaceFolder+file.split(workspaceFolder)[1];			
						if(getFileExtension(file) === 'py'){
							
							let sourceCode = getFileContentsFromPath(file);
		
							if (sourceCode != null) {
								const script = spawn('python', [__dirname+"/py-scripts/refactor.py",sourceCode]);
								script.stdout.on('data', function(data){
									writeFile(file,data.toString(),'utf-8',function(err){
										console.log("refactor is done")
									})
								})
							}
						}
					//}
				} catch(error){ vscode.window.showErrorMessage("could not read file - "+ file); }
			})
		}
	})
}

function makeWarningsVisibleInNotification(warnings) {
	try{
		warnings = warnings.split("\n");
		warnings.pop();
		warnings.forEach(warning => {
			try{
				if(!warning.includes("filename") && !warning.includes("error")){
					outputChannel.append(warning+"\n")
				}
				
			}catch(e){console.log(e);}
		});
		outputChannel.show();

	}catch(e){ console.log(e);};
}

const getAllFiles = function(dirPath, arrayOfFiles) {
	let files = fs.readdirSync(dirPath)
  
	arrayOfFiles = arrayOfFiles || []
  
	files.forEach(function(file) {
	  if (fs.statSync(dirPath + "/" + file).isDirectory()) {
		arrayOfFiles = getAllFiles(dirPath + "/" + file, arrayOfFiles)
	  } else {
		// arrayOfFiles.push(path.join(__dirname, dirPath, "/", file))
		arrayOfFiles.push(path.join(dirPath, "/", file))
	  }
	})
  
	return arrayOfFiles
}

const getFileContentsFromPath = (filepath) => {
	try{
		let code = fs.readFileSync(filepath);
		return code;
	}
	catch(e){console.log(e);}
}

const getFileExtension = (value) => {
	let pathSplits = value.split(".");
	return pathSplits[pathSplits.length - 1]? pathSplits[pathSplits.length - 1]: undefined;
}

const checkIfFilePath = (value) => {
	let pathSplits = value.split("/");
	return pathSplits[pathSplits.length - 1].includes(".")? true: false;
}

function deactivate() {}

module.exports = {
	activate,
	deactivate
}