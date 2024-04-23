export default interface ReactiveEvent {
    date: string,
    type: "DATA_PORTION" | "EVENT_INFO",
    payload: any
}
