import './App.css'
import GenerateVideo from "./GenerateVideo"
import axios from 'axios';

import React, { Component, useState, useEffect } from 'react';

class App extends Component {

  state = {
    // Initially, no file is selected
    selectedFile: null,
    downloadFile: null
  };

  // On file select (from the pop up)
  onFileChange = event => {
    // Update the state
    this.setState({ selectedFile: event.target.files[0] });
  };

  // On file upload (click the upload button)
  onFileUpload = () => {

    // Create an object of formData
    const formData = new FormData();

    // Update the formData object
    formData.append(
      "myFile",
      this.state.selectedFile,
      this.state.selectedFile.name
    );

    // Details of the uploaded file
    console.log(this.state.selectedFile);

    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    }).then((response) => {
      response.json().then((body) => {
        console.log("hehee")
        this.setState({ selectedFile: formData });
      });
    });

  };



  // File content to be displayed after
  // file upload is complete
  fileData = () => {
    if (this.state.selectedFile) {
      return (
        <div>
          <h2>File Details:</h2>

          <p>File Name: {this.state.selectedFile.name}</p>
          <p>File Type: {this.state.selectedFile.type}</p>
          <p>
            Last Modified:{" "}
            {this.state.selectedFile.lastModifiedDate.toDateString()}
          </p>

        </div>
      );
    } else {
      return (
        <div>
          <br />
          <h4>Choose before pressing the upload button</h4>
        </div>
      );
    }
  };

  onDownload = () => {

  }

  getDownloadFile = () => {

    let headers = new Headers();

    headers.append('Access-Control-Allow-Origin', "*");
    headers.append('Access-Control-Allow-Credentials', 'true');
    headers.append('Content-Type', 'application/octet-stream');
    headers.append('Accept', 'application/json');
    headers.append('Access-Control-Allow-Methods', "OPTIONS, POST, GET")

    fetch('http://localhost:5000/download', {
      method: 'POST',
      headers: headers,
    })
      .then((response) => response.blob())
      .then((blob) => {
        // Create blob link to download
        const url = window.URL.createObjectURL(
          new Blob([blob]),
        );

        console.log(url)
        const link = document.createElement('a');
        link.href = `your_link.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // const link = document.createElement('a');
        // link.href = url;
        // link.setAttribute(
        //   'download',
        //   `downloadTest.pdf`,
        // );

        // // Append to html link element page
        // document.body.appendChild(link);

        // // Start download
        // link.click();

        // // Clean up and remove the link
        // link.parentNode.removeChild(link);
      });
  }

  onGenerate = async () => {
    const response = await fetch("http://127.0.0.1:5000/generate", {
      method: "POST",
      headers: { "Access-Control-Allow-Origin": "*" }
    });
    if (response.ok) {
      console.log("it worked!");
    }
  };

  render() {

    return (
      <div>

        <h3>
          Upload your video here!
        </h3>

        <div>
          <input type="file" onChange={this.onFileChange} />
          <button onClick={this.onFileUpload}>
            Upload!
          </button>
        </div>

        {this.fileData()}
        <GenerateVideo />

        <div>
          <button onClick={() => { this.getDownloadFile() }}>
            Download Video
          </button>
        </div>
      </div>
    );
  }
}

export default App;
