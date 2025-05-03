export let dx = 0;
export let dy = 0;

export{handleKeyDown, handleKeyUp};

//Handles user inputs for sprite changes
function handleKeyDown(event){
if(event.key === "ArrowUp")
{
    dy--;

}
else if (event.key === "ArrowDown")
{
    dy++;

}
else if (event.key === "ArrowLeft")
{
    dx--;

}
else if (event.key === "ArrowRight")
{
    dx++;

}
}

 function handleKeyUp(event) {
   if (
     event.key === "ArrowUp" ||
     event.key === "ArrowDown" ||
     event.key === "ArrowLeft" ||
     event.key === "ArrowRight"
   ) {
     dx = 0;
     dy = 0;
   }
 }
