import './Homepage.css'
import Cookies from 'universal-cookie';
import GenerateVideo from "./GenerateVideo"
import DisplayAudios from './DisplayAudios';

import React, { Component, useState, useEffect } from 'react';
import { getCookieUserId, getCookieUsername } from './CookieUtils';
import {QueryClient, QueryClientProvider} from 'react-query'
import { checkLoggedIn, welcomePage } from './Welcome';
import { backendUrl } from './Conf';
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

    fetch(backendUrl+'/upload', {
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
          <h2 className='upload-title'>File Details:</h2>
          <p className='upload-text'>File Name: {this.state.selectedFile.name}</p>
          <p className='upload-text'> File Type: {this.state.selectedFile.type}</p>
        </div>
      );
    } else {
      return (
        <div>
          <h4 className='upload-title'>Choose before pressing the upload button</h4>
        </div>
      );
    }
  };

  onDownload = () => {

  }

  

  onGenerate = async () => {
    const response = await fetch(backendUrl+"/generate", {
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
        <h3 className='upload-title'>
          Upload your song here!
        </h3>

        <div>
          <input type="file" onChange={this.onFileChange} class="upload-file"/>
        </div>
        
        {this.fileData()}
        {/* <GenerateVideo /> */}
        <div class="button-container"><button onClick={this.onFileUpload}  class="upload-button"><p>Upload</p></button></div>
        
        <QueryClientProvider client={queryClient} contextSharing={true}><DisplayAudios /></QueryClientProvider>
      </div>
    );
  }
}

export default Homepage;
