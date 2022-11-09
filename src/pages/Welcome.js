import { getCookieUsername, logOut } from "./CookieUtils";

const checkLoggedIn = () => {
    const username = getCookieUsername();
    if (username == null) {
        return (<div>Please <a href='/login'>Login</a> or <a href='/registration'>Register</a></div>)
    } else {
        return (<div>
                    <div>
                        Welcome {username}! Start your journey from our <a href='/home'>Home Page</a>
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
            Welcome to LyricAl! We are ....
            {checkLoggedIn()}
        </div>
    );

}

export {welcomePage, checkLoggedIn}; 