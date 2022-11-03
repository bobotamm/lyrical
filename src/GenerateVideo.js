import React from "react";


const GenerateButton = (file) => {
    if (!file) {
        console.log("no file is selected");
        return
    }
    const handleSubmit = async() => {
        const response = await fetch ("http://127.0.0.1:5000/generate", {
            method: "POST",
            body: file,
            headers: {
                // "Access-Control-Allow-Origin": "*",
                "content-type": "multipart/form-data",
            },
        });
        if (response.ok){
            console.log("it worked!")
        }
    }

    return (
        <div>
            <button onClick = {handleSubmit}>Generate the Video!</button>
        </div>
    );

}

export default GenerateButton; 
