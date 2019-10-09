
document.addEventListener("DOMContentLoaded", function(){

    function clearElements(myNode)
    {
        while (myNode.firstChild) {
            myNode.removeChild(myNode.firstChild);
        }
    }
    function refreshObjectives()
    {
        request = new XMLHttpRequest();
        request.open("GET", "/api/objective")
        request.onload = function() {
            const myNode = document.getElementById("currentObjectives");
            clearElements(myNode);
            const objectives = JSON.parse(request.responseText);
            for (objective of objectives.objectives)
            {
                var listElement = document.createElement("LI");
                var textNode = document.createTextNode(objective.goal + " " + objective.expression);
                listElement.appendChild(textNode);
                myNode.appendChild(listElement);
            }
        };
        request.send();
    }

    function refreshConstraints()
    {
        cRequest = new XMLHttpRequest();
        cRequest.open("GET", "/api/constraint")
        cRequest.onload = function() {
            const myNode = document.getElementById("currentConstraints");
            clearElements(myNode);
            const constraints = JSON.parse(cRequest.responseText);
            for (constraint of constraints.constraints)
            {
                var listElement = document.createElement("LI");
                var textNode = document.createTextNode(constraint.left + " " + constraint.sign + " " + constraint.right);
                listElement.appendChild(textNode);
                myNode.appendChild(listElement);
            }
        };
        cRequest.send();
    }

    function refreshVariables()
    {
        vRequest = new XMLHttpRequest();
        vRequest.open("GET", "/api/variables")
        vRequest.onload = function() {
            const myNode = document.getElementById("currentVariables");
            clearElements(myNode);
            const variables = JSON.parse(vRequest.responseText);
            for (variable of variables.variables)
            {
                var listElement = document.createElement("LI");
                var textNode = document.createTextNode(
                    variable.name + ", type=" + variable.type + ", inverted=" + variable.isInverted);
                listElement.appendChild(textNode);
                myNode.appendChild(listElement);
            }
        };
        vRequest.send();
    }

    let resetButton = document.getElementById("reset");
    resetButton.addEventListener('click', (event) => {
        event.preventDefault();
        rRequest = new XMLHttpRequest();
        rRequest.open("POST", "/api/reset")
        rRequest.send()
        rRequest.onload = function() {
            document.getElementById("objectiveExpression").value = "";
            document.getElementById("constraintLeft").value = "";
            document.getElementById("constraintRight").value = "";
            refreshObjectives();
            refreshConstraints();
            refreshVariables();
            const myNode = document.getElementById("solutionValues");
            clearElements(myNode);
        };
    });

    let addObjectiveButton = document.getElementById("addObjective");
    addObjectiveButton.addEventListener('click', (event) => {
        event.preventDefault();
        var objectiveExpression = document.getElementById("objectiveExpression").value;
        var objectiveGoal = document.getElementById("objectiveGoal").value;
        oRequest = new XMLHttpRequest();
        oRequest.open("POST", "/api/objective/add")
        oRequest.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        oRequest.send(JSON.stringify({"expression": objectiveExpression, "goal": objectiveGoal}))
        oRequest.onload = function() {
            document.getElementById("objectiveExpression").value = "";
            refreshObjectives();
            refreshVariables();
        };
    });

    let addConstraintButton = document.getElementById("addConstraint");
    addConstraintButton.addEventListener('click', (event) => {
        event.preventDefault();
        var constraintLeft = document.getElementById("constraintLeft").value;
        var constraingSign = document.getElementById("constraintSign").value;
        var constraintRight = document.getElementById("constraintRight").value;

        consRequest = new XMLHttpRequest();
        consRequest.open("POST", "/api/constraint/add")
        consRequest.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        consRequest.send(JSON.stringify({"right": constraintRight, "left": constraintLeft, "sign": constraingSign}))
        consRequest.onload = function() {
            document.getElementById("constraintLeft").value = "";
            document.getElementById("constraintRight").value = "";
            refreshConstraints();
            refreshVariables();
        };
    });

    let setVariableButton = document.getElementById("setVariable");
    setVariableButton.addEventListener('click', (event) => {
        event.preventDefault();
        var varName = document.getElementById("varName").value;
        var isInverted = document.getElementById("varInverted").checked;

        consRequest = new XMLHttpRequest();
        consRequest.open("POST", "/api/variables/set")
        consRequest.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        consRequest.send(JSON.stringify({'name': varName, 'inverted': isInverted}))
        consRequest.onload = function() {
            document.getElementById("varName").value = "";
            document.getElementById("varInverted").checked = false;
            refreshVariables();
        };
    });

    let solveButton = document.getElementById("solve");
    solveButton.addEventListener('click', (event) => {
        event.preventDefault();
        var method = document.getElementById("solverMethod").value;
        // var debug = document.getElementById("solverDebug").checked;
         var debug = false;
        solveRequest = new XMLHttpRequest();
        solveRequest.open("POST", "/api/solve")
        solveRequest.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        solveRequest.send(JSON.stringify({"method": method, "debug": debug}))
        solveRequest.onload = function() {
            const myNode = document.getElementById("solutionValues");
            clearElements(myNode);
            const solution = JSON.parse(solveRequest.responseText);
            for (var key in solution.vars)
            {
                var listElement = document.createElement("LI");
                var textNode = document.createTextNode(key + " = " + solution.vars[key]);
                listElement.appendChild(textNode);
                myNode.appendChild(listElement);
            }
        };
    });
    refreshObjectives();
    refreshConstraints();
    refreshVariables();
})
