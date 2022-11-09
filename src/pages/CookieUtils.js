import Cookies from 'universal-cookie';

export function getCookieUsername(){
    const cookies = new Cookies();
    return cookies.get("lyrical_username")
}

export function setUsernameId(username, id){
    const cookies = new Cookies();
    cookies.set('lyrical_username', username, { path: '/' });
    cookies.set('lyrical_id', id, {path: '/'})
}

export function logOut() {
    console.log("Logging out")
    const cookies = new Cookies();
    cookies.remove('lyrical_username');
    cookies.remove('lyrical_id');
    window.location.href = "/";
}