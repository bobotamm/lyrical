import { getCookieUsername, logOut } from "./CookieUtils";
import './Welcome.css'

const checkLoggedIn = () => {
    const username = getCookieUsername();
    if (username == null) {
        return (<div className="login-check">To start, please <a href='/login'>Login</a> or <a href='/registration'>Register</a></div>)
    } else {
        return (<div className="login-check">
                    <div className="login-check">
                        Welcome {username}! <a href='/home'>Home Page</a>
                    </div>
                    <div>
                        <button onClick={logOut}>Log Out</button>
                    </div>
                </div>)
    }
}

const welcomePage = () => {
    return (
        <div>
            <div className="welcome-title">Welcome to LyricAl!</div>
            <div className="welcome-desc">LyricAl is a software made for musicians that specializes in producing stunning artwork to accompany any song.<br></br> Just upload the audio file of your choosing and we will take care of the rest!</div>
            <div>{checkLoggedIn()}</div>
        </div>
    );

}

export {welcomePage, checkLoggedIn}; 