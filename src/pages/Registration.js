import React, { useState } from 'react';
import { backendUrl } from './Conf';
import { setUsernameId } from './CookieUtils';

const Registration = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
  
    const userRegistration = async () => {
        console.log(username, password);
        const response = await fetch(backendUrl+"/register", {
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" },
        body: JSON.stringify({"username":username, "password":password})}).then(
            res => res.json()).then(responseData => {
            if (responseData['result'] == true) {
                setUsernameId(username, responseData['id'])
                window.location.href = "/home";
            } else {
                console.log("Bad");
                alert("Please use another username or password!");
            }
        }).catch(error => {
            alert(error);
        })
    };


    return (
        <div>
        <h3 className="center">Registration</h3>
        <div className="container">
          <div className="forms">
            <div className="form signup">
              <form action="#">
                <div className="input-field">
                  <input
                    type="text"
                    placeholder="Enter your username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
                <div className="input-field">
                  <input
                    type="password"
                    className="password"
                    placeholder="Create a password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                <div className="input-field button">
                  <input
                    type="button"
                    defaultValue="Register"
                    onClick={() => userRegistration()}
                  />
                </div>
              </form>
            </div>
          </div>
        </div>
        <a href='/'>Back</a>
      </div>
    );
  }
  
  export default Registration;