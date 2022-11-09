import { useState } from 'react';
import { setUsernameId } from './CookieUtils';

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
  
    const userLogin = async () => {
        console.log(username, password);
        const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: { "Access-Control-Allow-Origin": "*" },
            body: JSON.stringify({"username":username, "password":password})
        }).then(
            res => res.json()).then(responseData => {
            if (responseData['result'] == true) {
                setUsernameId(username, responseData['id'])
                window.location.href = "/home";
            } else {
                alert("Log in Failed!");
            }
        }).catch(error => {
            alert(error);
        })
    };


    return (
        <div>
        <h3 className="center">Login</h3>
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
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                <div className="input-field button">
                  <input
                    type="button"
                    defaultValue="Login"
                    onClick={() => userLogin()}
                  />
                </div>
              </form>
              <div className="login-signup">
                <span className="text">
                  Not an existing user?  
                  <a href="/registration" className="text login-link">
                    Signup now
                  </a>
                </span>
              </div>
            </div>
          </div>
        </div>
        <a href='/'>Back</a>
      </div>
    );
  }
  
  export default Login;