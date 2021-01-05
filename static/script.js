/* When you mark a task as being 'Done' or 'Not Done' this button switches the button style and text */
function check(id)
{
    if (document.getElementById(id).innerHTML === 'Done')
    {
        document.getElementById(id).style.backgroundColor='#ADAD42';
        document.getElementById(id).innerHTML = 'Not Done';
    }
    else if (document.getElementById(id).innerHTML === 'Not Done')
    {
        document.getElementById(id).style.backgroundColor='A63D40';
        document.getElementById(id).innerHTML = 'Done';
    }
}

/* This function sets the value of an element to 'delete', when the page is refreshed the server checks for this value and deletes the item from the SQL table */
function remove(id)
{
    console.log(document.getElementById(id));
    document.getElementById(id).value = 'delete';
    console.log(document.getElementById(id));
}

/* Display the value of the range slider when you rate your day */
function updateRangeInput(val)
{
    document.getElementById('value').innerHTML = val;
}

/* Expands a popup of the selected teble element */
function expandForm(id)
{
    document.getElementsByClassName(id)[0].style.display = 'block';
    /* Scrolls to popup */
    document.getElementsByClassName(id)[0].scrollIntoView();
}

/* Closes the expanding popup */
function closeForm(id)
{
    document.getElementsByClassName(id)[0].style.display = 'none';
}

/* Makes hidden 'Completed' tasks visible or hides them deppending on the check button */
function filter(id)
{
    var checkBox = document.getElementById('filter');
    var row = document.getElementsByClassName(id)
    for (let i = 0; i < row.length; i++)
    {
        if (checkBox.checked == true)
        {
            row[i].style.display = '';
        }
        else if (checkBox.checked == false)
        {
            row[i].style.display = 'none';
        }
    }
}