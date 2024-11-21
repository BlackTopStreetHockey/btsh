"use client";

import { useState, useEffect } from "react";

const promiseRequest = ({
  route,
  method='GET',
  params=undefined, // request args
  body=undefined, // post/put body
  controller=undefined
}) => {
  const promise = new Promise((resolve, reject) => {
    const url = `${process.env.API_URL}/api/${route}/`;
    const args = !!params ? `?${new URLSearchParams(params).toString()}` : '';
    fetch(`${url}${args}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: !!body ? JSON.stringify(body) : undefined,
      signal: controller?.signal,
    }).then(async (res) => {
      if (res.status >= 400) {
        console.error(`Received error (${res.status}): ${res.statusText}`)
        reject(res)
      } 
      resolve(await res.json())
    }).catch(async (error) => {
      console.error(error)
      reject(error)
    });
  });
  return promise;
}

function useRequest({
  route,
  method='GET',
  params={},
  body=undefined,
  skip=false, // if true, won't fire request
}) {
  let controller;
  const [state, setState] = useState({ data: undefined, loading: !skip, error: undefined });
  const fetchData = () => {
    if (skip) return;
    controller = new AbortController();
    setState({ loading: true, data: undefined, error: undefined  })
    const promise = promiseRequest({
      route,
      method,
      params,
      body,
      controller
    })
    promise.then(res => {
      setState({ loading: false, data: res, error: undefined })
    }).catch(err => {
      setState({ loading: false, data: undefined, error: err })
    });
  }

  useEffect(() => {
    fetchData();
    return () => {
      controller?.abort();
    }
  }, [skip, JSON.stringify(body), JSON.stringify(params)]);

  return state;
}

export { useRequest };
