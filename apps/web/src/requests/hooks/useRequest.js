"use client";

import { useState, useEffect } from "react";

const promiseRequest = ({
  route,
  method='GET',
  params=undefined, // request args
  body=undefined, // post/put body
}) => {
  let controller = new AbortController();
  const promise = new Promise((resolve, reject) => {
    const url = `${process.env.API_URL}/api/${route}`;
    const args = !!params ? `?${new URLSearchParams(params).toString()}` : '';
    fetch(`${url}${args}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: !!body ? JSON.stringify(body) : undefined,
      signal: controller.signal,
    }).then(async (res) => {
      if (res.status >= 400) {
        reject(res)
      } 
      resolve(await res.json())
    }).catch(async (error) => {
      reject(error)
    });
  });
  return [promise, controller]
}

function useRequest({
  route,
  method='GET',
  params={},
  body=undefined,
  skip=false, // if true, won't fire request
}) {
  const [state, setState] = useState({ data: undefined, loading: !skip, error: undefined });
  const fetchData = () => {
    if (skip) return;
    setState({ loading: true, data: undefined, error: undefined })
    const [promise, controller] = promiseRequest({
      route,
      method,
      params,
      body
    })
    promise.then(res => {
      setState({ loading: false, data: res, error: undefined })
    }).catch(err => {
      setState({ loading: false, data: undefined, error: err })
    });
    return controller
  }

  useEffect(() => {
    var cntrl;
    cntrl = fetchData()
    return () => {
      if (!!cntrl) {
        cntrl.abort();
      }
    }
  }, [skip]);
  
  return {
    ...state
  }
}

export { useRequest };
// async function getGameDays(
//   month: number,
//   year: number
// ): Promise<GameDaysResponse> {
//   const cacheKey = `${month}-${year}`;
  
//   // Return cached request if it exists
//   if (await requestCache[cacheKey]) {
//     return requestCache[cacheKey];
//   }

//   // Create the request promise
//   const requestPromise = new Promise<GameDaysResponse>(async (resolve, reject) => {
//     try {
//       const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/game_days`);
//       if (!res.ok) {
//         throw new Error(`Failed to fetch game days: ${res.statusText}`);
//       }
//       const data = await res.json();
//       resolve(data);
//     } catch (error) {
//       console.error("Error fetching game days:", error);
//       // Remove failed request from cache
//       delete requestCache[cacheKey];
//       reject(error);
//     }
//   });

//   // Store in cache
//   requestCache[cacheKey] = requestPromise;
//   return requestPromise;
// }