
import React, { useEffect, useState } from "react";
import {QueryClient, useQuery} from 'react-query'
import { backendUrl } from "./Conf";
import { getCookieUserId } from "./CookieUtils";
import {Download} from "./Download"
import './Homepage.css'
import './DisplayAudios.css'


async function fetchAudioData() {
  const userId = getCookieUserId();
  if (userId == null) {
    return null;
  }
  console.log('Fetching Uploaded Audio Files')
  const data = await fetch(backendUrl+"/display", {
  method: "POST",
  headers: { "Access-Control-Allow-Origin": "*" },
  body: JSON.stringify({"user_id": userId})
  })
  .then((res) => res.json())
  .then((json) => {
          return json['audio_data'];
      });
  return data;
};

function interpretStatus(status, audioId) {
  if (status == 0) {
    return "In Queue"
  }
  if (status == 1) {
    return "Generating"
  }
  if (status == 2) {
    const userId = getCookieUserId();
    const audioIdCopy = audioId;
    return (Download(userId, audioIdCopy))
  }
}

function DisplayAudios(){
    const {data, error, isError, isLoading } = useQuery('audio', fetchAudioData,{fetchPolicy: 'cache-and-network'})
    if (!data || isLoading) {
      return <div className="upload-title">Loading!</div>;
    }
    if (isError) {
      return <div className="upload-title">Error</div>
    }
    return (<>
    <h3 className="upload-title">
      These are the files you have uploaded! <br></br> A download button would appear when the video is ready!
    </h3>
    <div className="button-container">
      <table className="display-table">
        <thead className="display-thead">
          <tr>
            <th><span className="table-text">File Name</span></th>
            <th><span className="table-text">Status</span></th>
          </tr>
        </thead>
        <tbody>
          {/* iterate through the customers array and render a unique Customer component for each customer object in the array */}
          { data.map(d => <tr><td><span className="table-text">{d[1]}</span></td><td><span className="table-text">{interpretStatus(d[2], d[0])}</span></td></tr>) }
        </tbody>
      </table>
    </div>
    </>)
}
export default DisplayAudios;