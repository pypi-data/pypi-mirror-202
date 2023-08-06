// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module roboweb-extension
 */
import { IThemeManager } from '@jupyterlab/apputils';
import { ITranslator } from '@jupyterlab/translation';
import { NotebookActions, INotebookTracker } from '@jupyterlab/notebook';
import { Widget } from '@lumino/widgets';
import { ICommandPalette } from '@jupyterlab/apputils';

class AssistantSidebar extends Widget {
  constructor() {
    super();
    this.id = 'assistant-panel';
    this.addClass('assistant-panel');
    this.title.caption = 'Assistant';
    this.title.iconClass = 'fa fa-robot';
  }
}

function waitForNonNullVariable(reader, callback) {
  var variable = reader(); 
  if (variable !== null) {
    callback(variable);
  } else {
    setTimeout(function() {
      waitForNonNullVariable(reader, callback);
    }, 100); // Wait 1 second before checking again
  }
}

function levenshteinDistance(a, b) {
  const matrix = [];

  if (a.length === 0) return b.length;
  if (b.length === 0) return a.length;

  for (let i = 0; i <= b.length; i++) {
    matrix[i] = [i];
  }

  for (let j = 0; j <= a.length; j++) {
    matrix[0][j] = j;
  }

  for (let i = 1; i <= b.length; i++) {
    for (let j = 1; j <= a.length; j++) {
      if (b.charAt(i - 1) === a.charAt(j - 1)) {
        matrix[i][j] = matrix[i - 1][j - 1];
      } else {
        matrix[i][j] = Math.min(matrix[i - 1][j - 1] + 1, // substitution
                                Math.min(matrix[i][j - 1] + 1, // insertion
                                         matrix[i - 1][j] + 1)); // deletion
      }
    }
  }

  return matrix[b.length][a.length];
}

function similarity(a, b) {
  const distance = levenshteinDistance(a, b);
  const maxLength = Math.max(a.length, b.length);
  return (maxLength - distance) / maxLength;
}

function replaceCurrentCell(tracker, code) {
  const currentNotebook = tracker.currentWidget;
  if (!currentNotebook) {
    return;
  }
  code = code.trim();

  //iterate over all cells and find the one with the highest similarity
  var maxSimilarity = 0;
  var maxIndex = -1;
  var lastEmptyCell = -1; 
  var lastCellWithExclamationMark = -1;
  //remove lines with python comments from code
  const codeMinusComments = code.split("\n").filter(function(line) {
    return !line.startsWith("#");
  }).join("\n");

  for (var i = 0; i < currentNotebook.content.model.cells.length; i++) {
    const cell = currentNotebook.content.model.cells.get(i);
    const cellContent = cell.value.text;
    if (cellContent.includes(codeMinusComments)) {
      return; 
    }
    if (cellContent.trim().length == 0) {
      lastEmptyCell = i;
    }
    const similarityValue = similarity(cellContent, code);
    if (similarityValue > maxSimilarity) {
      maxSimilarity = similarityValue;
      maxIndex = i;
    }
    if (cellContent.startsWith("!")) {
      lastCellWithExclamationMark = i;
    }
  }
  if (maxSimilarity > 0.8) {
    const cell = currentNotebook.content.model.cells.get(maxIndex);
    cell.value.text = code;
  } else {
    //find the index of the last cell that starts with ! and add the cell after it
    if (code.startsWith("!")) {
      //add cell at the beginning of the notebook
      const cell = currentNotebook.content.model.contentFactory.createCodeCell({});
      cell.value.text = code;
      currentNotebook.content.model.cells.insert(0, cell);
    } else if (code.startsWith("%") && !code.startsWith("%%")) {
        const cell = currentNotebook.content.model.contentFactory.createCodeCell({});
        cell.value.text = code;
        currentNotebook.content.model.cells.insert(lastCellWithExclamationMark + 1, cell);
    } else if (lastEmptyCell != -1) {
      const cell = currentNotebook.content.model.cells.get(lastEmptyCell);
      cell.value.text = code; 
    } else {
      const cell = currentNotebook.content.model.contentFactory.createCodeCell({});
      cell.value.text = code;
      currentNotebook.content.model.cells.push(cell);
    }
  }
};

function removeAnsiCodes(str) {
  return str.replace(/\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])/g, '');
}

function getCellContent(cell) {
  var outputText = "";
  const outputJSON = cell.outputArea.model.toJSON();
  if (outputJSON.length > 0) {
    const traceback = outputJSON[0].traceback;
    if (traceback != null) {
      for (var i = 0; i < traceback.length; i++) {
        const escapeRegex = /\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]/g;
        const plainTextString = traceback[i].replace(escapeRegex, '');
        outputText += plainTextString + "\n";
      }
    } else {
      outputText = outputJSON[0].text;
    }
  }

  return {
    "text": cell.model.value.text,
    "output": removeAnsiCodes(outputText)
  }
}
function getCurrentCellContent(tracker, app) {
  const currentNotebook = tracker.currentWidget;
  if (!currentNotebook) {
    return;
  }
  //get index of currently selected cell
  const index = currentNotebook.content.activeCellIndex;
  if (index === -1) {
    return "";
  } else {
    //retrieve cell text including its kernel output
    const current = app.shell.currentWidget.content.activeCell; 
    return getCellContent(current); 
  }
}

function loadFlutterApp() {
  window.isJupyter = true;
  window.serviceWorkerVersion = "124778936";
  const flutter_script = document.createElement('script');
  flutter_script.src = '/roboweb-server-extension/flutter.js';
  document.head.appendChild(flutter_script);
  
  flutter_script.onload = function() {
    console.log('Downloading main.dart.js');
    _flutter.loader.loadEntrypoint({
      serviceWorker: {
        serviceWorkerVersion: serviceWorkerVersion,
      }
    }).then(function(engineInitializer) {
      console.log('Initializing engine');
      waitForNonNullVariable(function() {return document.getElementById("assistant-panel")}, function (target) {
        engineInitializer.initializeEngine({
          hostElement: target,
        }).then(function(appRunner) {
          return appRunner.runApp();
        })
      }); 
      //if target is null sleep for 100 ms 
    });
  };
}
const plugin = {
    id: 'roboweb-extension',
    requires: [INotebookTracker, ICommandPalette, IThemeManager],
    activate: (app, tracker, palette, manager) => {
      console.log(
        'Roboweb extension activated v0.1'
      );
      const widget = new AssistantSidebar();
      widget.node.style.minWidth = "450px";
      app.shell.add(widget, 'right', { rank: 0 });
      
      window.enableThemeSync = true;

      manager.themeChanged.connect((_, args) => {
        if (window.enableThemeSync) {
          window.changeThemeFlutter(args.newValue);
        } else {
          window.enableThemeSync = true;
        }
      });
      window.getCurrentJupyterTheme = function() {
        return manager.theme;
      }
      window.changeThemeJupyter = function(theme) {
        manager.setTheme(theme);
        window.enableThemeSync = false;
      }
      //register function to retrieve current cell text
      window.currentCellText = function () {
        return getCurrentCellContent(tracker, app);
      }

      //register function to edit current cell text
      window.replaceCodeCurrentCell = function(code) {
        replaceCurrentCell(tracker, code);
      }
      window.runAll = function() {
        const currentNotebook = tracker.currentWidget;
        if (!currentNotebook) {
          return;
        }
        NotebookActions.runAll(currentNotebook.content, currentNotebook.sessionContext);
      }
  
      //track and log executions 
      NotebookActions.executed.connect(async (_, args) => {
        const { cell, notebook, success, error } = args;
        var cellContent = getCellContent(cell); 
        const input = cellContent.text;
        const output = cellContent.output;
        console.log("Output: " + output);
        window.logCellExecution(cellContent.text, cellContent.output);
        if (error) {
          window.autoPrompt(cellContent.text, cellContent.output);
        } 
      });

      app.commands.addCommand('fix-cell-extension:fixCell', {
        label: 'Fix',
        execute: () => {
          const currentNotebook = tracker.currentWidget;
          if (!currentNotebook) {
            return;
          }
          const currentCell = window.currentCellText();
          const errorPrompt = "My code has an error. \n\nCode: \n\n" + currentCell.text + "\n\nError: \n\n" + currentCell.output;
          window.pastePrompt(errorPrompt); 
        }
      });
    
      app.contextMenu.addItem({
        command: 'fix-cell-extension:fixCell',
        selector: '.jp-Notebook',
        rank: 0
      });  

      window.addEventListener('click', function(event) {
        const assistantPanelDiv = document.querySelector('#assistant-panel');
        if (!assistantPanelDiv.contains(event.target)) {
          removeFocus();
        }
      
      }, { passive: true });
            

      //embed flutter app 
      loadFlutterApp();
    },
    autoStart: true
};
export default plugin;



