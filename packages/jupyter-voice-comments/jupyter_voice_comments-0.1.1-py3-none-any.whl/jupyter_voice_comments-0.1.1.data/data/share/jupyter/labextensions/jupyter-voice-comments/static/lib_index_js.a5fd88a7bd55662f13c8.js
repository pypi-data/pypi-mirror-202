"use strict";
(self["webpackChunkjupyter_voice_comments"] = self["webpackChunkjupyter_voice_comments"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");



/**
 * Initialization data for the jupyter-voice-comments extension.
 */
const plugin = {
    id: 'jupyter-voice-comments:plugin',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    activate: (app, notebookTracker) => {
        console.log('JupyterLab extension jupyter-voice-comments is activated!');
        // Web Speech API initialization
        const SpeechRecognition = window.SpeechRecognition ||
            window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        let isRecording = false;
        const toggleRecording = () => {
            const button = document.getElementById('lm-VoiceWidget-button');
            const buttonStyle = button.style;
            const resetStyles = () => {
                buttonStyle.backgroundColor = 'rgb(224, 224, 224)';
                buttonStyle.outline = '2px solid rgb(224, 224, 224)';
            };
            const resetRecording = () => {
                isRecording = false;
                recognition.stop();
                resetStyles();
            };
            if (isRecording) {
                resetRecording();
            }
            else {
                recognition.start();
                isRecording = true;
                buttonStyle.backgroundColor = 'rgb(228, 99, 99)';
                buttonStyle.outline = '2px solid rgb(228, 99, 99)';
            }
        };
        // creates a new command that inserts a comment and fetches a code snippet from openai based on the comment
        app.commands.addCommand('jupyter-voice-comments:insert-comment', {
            label: 'Insert Comment',
            execute: (args) => {
                const { comment } = args;
                const current = notebookTracker.currentWidget;
                if (current) {
                    const notebook = current.content;
                    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.insertAbove(notebook);
                    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.changeCellType(notebook, 'markdown');
                    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.run(notebook);
                    const cell = notebook.activeCell;
                    if (cell) {
                        cell.model.value.text = comment;
                    }
                    /***********************************************
                     * Clean up the fetch request to openai below  *
                     * I plan to make it so that the fetch request *
                     * is made in a separate file                  *
                     **********************************************/
                    const url = 'https://q6ya2o2jm2.execute-api.us-east-2.amazonaws.com/default/jplext-voice-comments-openai';
                    const prompt = (0,_utils__WEBPACK_IMPORTED_MODULE_2__.openaiPrompt)(comment);
                    // async function that fetches a code snippet from openai based on the voice comment and creates a draggable modal with the code snippet
                    const fetchOPENAI = async () => {
                        const response = await fetch(url, {
                            method: 'POST',
                            body: JSON.stringify({ text: prompt })
                        });
                        const data = await response.json();
                        (0,_utils__WEBPACK_IMPORTED_MODULE_2__.dragElement)((0,_utils__WEBPACK_IMPORTED_MODULE_2__.createModal)(data.result));
                    };
                    fetchOPENAI();
                    /************************************************
                     * Add a loading spinner on the modal that is   *
                     * removed when the fetch request is complete.  *
                     * Create the function in a separate file.      *
                     ************************************************/
                }
                else {
                    console.log('No active notebook');
                }
            }
        });
        recognition.addEventListener('result', (event) => {
            const last = event.results.length - 1;
            const text = event.results[last][0].transcript;
            app.commands.execute('jupyter-voice-comments:insert-comment', {
                comment: text
            });
        });
        /******************************************************
         * Add a widget to the top of the JupyterLab window   *
         * that includes a button to toggle voice recording   *
         * on and off.                                        *
         * I also need to include the code snippet in the     *
         * widget. Also, add more user functionality to close *
         * the widget and modify the code snippet.            *
         ******************************************************/
        const widget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget();
        widget.id = 'lm-VoiceWidget';
        const button = document.createElement('button');
        button.id = 'lm-VoiceWidget-button';
        button.title = 'Toggle voice recording (Alt + V)';
        button.addEventListener('click', toggleRecording);
        document.addEventListener('keydown', (event) => {
            if (event.altKey && event.key === 'v') {
                toggleRecording();
            }
        });
        widget.node.appendChild(button);
        app.shell.add(widget, 'top');
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "createModal": () => (/* binding */ createModal),
/* harmony export */   "dragElement": () => (/* binding */ dragElement),
/* harmony export */   "openaiPrompt": () => (/* binding */ openaiPrompt)
/* harmony export */ });
// function to create modal
const createModal = (modalContent) => {
    const relativeElement = document.getElementsByClassName('jp-Notebook')[0];
    const modalContainer = document.createElement('div');
    modalContainer.id = 'lm-VoiceWidget-modalContainer';
    const modal = document.createElement('pre');
    modal.id = 'lm-VoiceWidget-modal';
    modal.textContent = modalContent !== null ? modalContent : '';
    modal.tabIndex = 0; // Add tabindex to make modal focusable
    modalContainer.appendChild(modal);
    relativeElement.appendChild(modalContainer); // Append modal to activeCell
    modal.focus(); // Focus on modal
    modal.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            modal.remove();
        }
        if (event.ctrlKey && event.key === 'c') {
            event.preventDefault();
            const text = modal.textContent;
            if (text) {
                navigator.clipboard.writeText(text);
            }
        }
    });
    modal.addEventListener('mousedown', (event) => {
        modal.focus(); // Give modal focus when clicked
    });
    dragElement(modalContainer);
    return modalContainer;
};
const dragElement = (ele) => {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    ele.onmousedown = dragMouseDown;
    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }
    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        ele.style.top = ele.offsetTop - pos2 + 'px';
        ele.style.left = ele.offsetLeft - pos1 + 'px';
    }
    function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
    }
};
const openaiPrompt = (comment) => {
    const prompt = `Give me a python code snippet based on the following comment: ${comment}. Do not include the comment in the code snippet. The code snippet should be a valid python code snippet. Do not include any examples of running the code in the snippet. Make sure that all new function definitions are on a new line, and follow proper Python formatting conventions. Make sure any helper functions that are needed for the code snippet are also definied in the snippet. This is for a JupyterLab extension that just uses the response from this prompt to display a code snippet modal. Users should be able to copy the code snippet from the modal and run it in their jupyter notebook.`;
    return prompt;
};


/***/ })

}]);
//# sourceMappingURL=lib_index_js.a5fd88a7bd55662f13c8.js.map