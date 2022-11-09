import './Homepage.css'
import Cookies from 'universal-cookie';
import GenerateVideo from "./GenerateVideo"
import DisplayAudios from './DisplayAudios';

import React, { Component, useState, useEffect } from 'react';
import { getCookieUserId, getCookieUsername } from './CookieUtils';
import {QueryClient, QueryClientProvider} from 'react-query'
import { checkLoggedIn, welcomePage } from './Welcome';
const queryClient = new QueryClient();
class Homepage extends Component {

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
    formData.append("user_id", getCookieUserId());

    // Details of the uploaded file
    console.log(this.state.selectedFile);

    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    }).then(res => res.json()).then(responseData => {
        if (responseData['result'] == true) {
            window.location.href = "/home"
        } else {
            alert("Upload Failed!");
        }
    }).catch(error => {
        alert(error);
    })
    // .then((response) => {
    //   response.json().then((body) => {
    //     this.setState({ selectedFile: formData });
    //   });
    // });

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
        </div>
      );
    } else {
      return (
        <div>
          <h4>Choose before pressing the upload button</h4>
        </div>
      );
    }
  };

  onDownload = () => {

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
    const username = getCookieUsername();
    if (username == null) {
      window.location.href = "/"
    }
    return (
      <div>
        {checkLoggedIn()}
        <h3>
          Upload your song here!
        </h3>

        <div>
          <input type="file" onChange={this.onFileChange} />
          <button onClick={this.onFileUpload}>
            Upload!
          </button>
        </div>
        {this.fileData()}
        {/* <GenerateVideo /> */}
        <QueryClientProvider client={queryClient} contextSharing={true}><DisplayAudios /></QueryClientProvider>
      </div>
    );
  }
}

export default Homepage;
