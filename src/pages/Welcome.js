import { getCookieUsername } from "./CookieUtils";

const checkLoggedIn = () => {
    const username = getCookieUsername();
    if (username == null) {
        return (<div>Please <a href='/login'>Login</a> or <a href='/registration'>Register</a></div>)
    } else {
        return (<div>Welcome {username}! Start your journey from our <a href='/home'>Home Page</a></div>)
    }
}

const GenerateButton = () => {
    return (
        <div>
            Welcome to LyricAl! We are ....
            {checkLoggedIn()}
        </div>
    );

}

export default GenerateButton; 