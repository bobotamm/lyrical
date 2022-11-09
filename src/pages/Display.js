import React, { useState } from 'react';
import {getCookieUsername, logOut} from "./CookieUtils.js"

const Display = () => {

    let display;
    const username = getCookieUsername();
    if (username != null) {
        display = (<div>Welcome {username}! <button onClick={logOut}>Log Out</button></div>)
    } else {
        display = (<div>Please <a href='/login'>Login</a> or <a href='/registration'>Register</a></div>)
    }
    return display
}
export default Display;
