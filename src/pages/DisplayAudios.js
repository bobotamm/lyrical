
import React, { useEffect, useState } from "react";
import {QueryClient, useQuery} from 'react-query'
import { backendUrl } from "./Conf";
import Download from "./Download"


async function fetchAudioData() {
  const userId = 1;
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
  return data
};

function interpretStatus(status) {
  if (status == 0) {
    return "In Queue"
  }
  if (status == 1) {
    return "Generating"
  }
  if (status == 2) {
    return (<Download></Download>)
  }
}

function DisplayAudios(){
    const {data, error, isError, isLoading } = useQuery('audio', fetchAudioData,{fetchPolicy: 'cache-and-network'})
    if (!data || isLoading) {
      return <div>Loading!</div>;
    }
    if (isError) {
      return <div>Error</div>
    }
    return (<>
    <div>
      These are the files you have uploaded! A download button would appear when the video is ready!
    </div>
    <table border="1">
      <thead>
        <tr>
          <th>File Name</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {/* iterate through the customers array and render a unique Customer component for each customer object in the array */}
        { data.map(d => <tr key={d[0]}><td>{d[1]}</td><td>{interpretStatus(d[2])}</td></tr>) }
      </tbody>
    </table>
    </>)
}
export default DisplayAudios;