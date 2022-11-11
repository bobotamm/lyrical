import { backendUrl } from "./Conf";

export function Download(userId, audioId) {
    const getDownloadFile = async () => {
        let headers = new Headers();
    
        headers.append('Access-Control-Allow-Origin', "*");
        headers.append('Access-Control-Allow-Credentials', 'true');
        headers.append('Content-Type', 'application/octet-stream');
        headers.append('Accept', 'application/json');
        headers.append('Access-Control-Allow-Methods', "OPTIONS, POST, GET")
        // TODO: Add particular audio id to download
        fetch(backendUrl+'/download', {
          method: 'POST',
          headers: headers,
          body: JSON.stringify({"audio_id": audioId, "user_id": userId})
        })
          .then((response) => response.blob())
          .then((blob) => {
            console.log(blob)
            // Create blob link to download
            const url = window.URL.createObjectURL(
              new Blob([blob]),
            );
            console.log(url)
            const link = document.createElement('a');
            link.href = url;
            // TODO: update name
            link.setAttribute(
              'download',
              `fancy_mv.mp4`,
            );
    
            // Append to html link element page
            document.body.appendChild(link);
    
            // Start download
            link.click();
    
            // Clean up and remove the link
            link.parentNode.removeChild(link);
          });
      }

    return (
        <div>
            <button onClick={() => { getDownloadFile() }}>
                Download Video
            </button>
        </div>
    );
}