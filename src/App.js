
import Button from '@material-ui/core/Button';
//import PhotoCamera from '@material-ui/icons/PhotoCamera';
//import IconButton from '@material-ui/core/IconButton';
import React from 'react'; //{useState, useEffect} from 'react';
//import axios from 'axios';
 

const App = () => {
 
  return (
    <div className='lyrical-upload'>
      <div style={{ width: '100%', float: 'center', padding: '25'}}>
        <h3>Upload your video here!</h3> <br />
      </div>
      <input 
        type="file"
        accept="image/*"
        style={{ display: 'none'}}
        id="contained-button-file"
      />
      <label htmlFor="contained-button-file">
        <Button variant="contained" color="primary" component="span">
          Upload
        </Button>
      </label>
    </div>
  );
}
 

export default App;
