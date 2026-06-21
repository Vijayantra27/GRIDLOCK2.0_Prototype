const API_URL = "https://gridlock2-0-prototype.onrender.com";

export const getHotspots = async () =>
  fetch(`${API_URL}/hotspots`)
    .then((res) => res.json());

export const getCongestion = async () =>
  fetch(`${API_URL}/congestion`)
    .then((res) => res.json());

export const getPatrol = async () =>
  fetch(`${API_URL}/patrol`)
    .then((res) => res.json());

export const getOfficers = async () =>
  fetch(`${API_URL}/officers`)
    .then((res) => res.json());

export const getDNA = async () =>
  fetch(`${API_URL}/dna`)
    .then((res) => res.json());

export const getPropagation = async () =>
  fetch(`${API_URL}/propagation`)
    .then((res) => res.json());

export const getRisk = async () =>
  fetch(`${API_URL}/risk`)
    .then((res) => res.json());

export const getSimulation = async () =>
  fetch(`${API_URL}/simulation`)
    .then((res) => res.json());

export const askAssistant = async (
  question: string
) =>
  fetch(
    `${API_URL}/assistant?q=${encodeURIComponent(question)}`
  ).then((res) => res.json());

export const getRoutes = async () =>
  fetch(`${API_URL}/routes`)
    .then((res) => res.json());

export const getEmerging = async () =>
  fetch(`${API_URL}/emerging`)
    .then((res) => res.json());

export const getDashboard = async () =>
  fetch(`${API_URL}/dashboard`)
    .then((res) => res.json());

export const optimizeRoute = async (
  clusters: number[],
  station: number
) =>
  fetch(`${API_URL}/optimize-route`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      clusters,
      station,
    }),
  }).then((res) => res.json());

export const getRecommendations =
async (station:number)=>

fetch(
`${API_URL}/recommend/${station}`
)
.then((res)=>res.json());

export const getOfficerRecommendation =
async (cluster:number)=>

fetch(
`${API_URL}/officer-recommendation/${cluster}`
)
.then((res)=>res.json());

export const getImpact =
async (cluster:number)=>

fetch(
`${API_URL}/impact/${cluster}`
)
.then((res)=>res.json());

export const getAdvisor =
async () =>
fetch(
`${API_URL}/advisor`
)
.then((res)=>res.json());

export const getCoverage =
async (
  selectedClusters:number[]
)=>

fetch(
`${API_URL}/coverage`,
{
  method:"POST",
  headers:{
    "Content-Type":
    "application/json"
  },
  body:JSON.stringify({
    selected_clusters:
    selectedClusters
  })
}
)
.then(res=>res.json());