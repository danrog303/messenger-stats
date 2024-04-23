import React, { useEffect, useState } from "react";
import {BarChart, PieChart} from "@mui/x-charts";
import { useParams } from "react-router-dom";
import { Box, Container, Grid } from "@mui/material";
import ReactiveEvent from "../../../models/ReactiveEvent";
import ChatStatsEntry from "../../../models/ChatStatEntry";

interface LogsEntry {
    timestamp: string;
    message: string;
}

// Maps event names returned by backend to human-readable messages
const logMap: Record<string, string> = {
    "unzip-start": "Unzipping the file...",
    "unzip-finish": "Unzipping completed.",
    "stats-read-start": "Reading statistics...",
    "stats-read-finish": "All statistics parsed.",
};

// Maps metric names returned by backend to human-readable headers
const chatMap: Record<string, string> = {
    "biggest-chat": "Number of chats with the most messages",
    "sent-from": "Number of messages sent by a user",
    "msg-types": "Type of media used",
    "yearly-graph": "Number of messages sent per year",
    "hourly-graph": "Number of messages sent per hour",
    "monthly-graph": "Number of messages sent per month",
    "minute-graph": "Number of messages sent per minute",
    "daily-graph": "Number of messages sent per day",
    "weekday-graph": "Number of messages sent per weekday",
    "chat-counts": "Number of groups you share with the person",
    "word-counts-3": "Most common 3-letter or more phrases",
    "word-counts-5": "Most common 5-letter or more phrases",
    "word-counts-7": "Most common 7-letter or more phrases"
};

export default function StatsPage() {
    const {key} = useParams<string>();

    const [logs, setLogs] = useState<LogsEntry[]>([]);
    const [stats, setStats] = useState<ChatStatsEntry[]>([]);

    useEffect(() => {
        const sse = new EventSource(`http://localhost:8080/stats/${key}`, { withCredentials: true });
        sse.onmessage = e => {
            const data = JSON.parse(e.data) as ReactiveEvent;
            if (data.type === "EVENT_INFO") {
                setLogs(prevState => [...prevState, { timestamp: data.date, message: data.payload }]);
            } else if (data.type === "DATA_PORTION") {
                setStats(prevState => [...prevState, data.payload]);
            }
        };
        sse.onerror = () => {
            sse.close();
        };
        return () => {
            sse.close();
        };
    }, []);

    function getGraphForMetrics(metrics: ChatStatsEntry) {
        // const pieChartSeriesConfig = [{
        //     data: Object.entries(metrics.metrics).map(([label, value]) => ({label, value}))}
        // ];
        const barChartSeriesConfig = [{
            data: Object.entries(metrics.metrics).map(([label, value]) => value)
        }];
        const barChartXAxisConfig = [{
            data: Object.entries(metrics.metrics).map(([label, value]) => label),
            scaleType: "band"
        }];

        return <div>
            <h3>{chatMap[metrics.type]}</h3>

            {/* @ts-ignore */}
            <BarChart series={barChartSeriesConfig} xAxis={barChartXAxisConfig} width={600} height={300} key={metrics.type}/>
        </div>
    }

    return (
        <Container>
            <Box>
                <h1>Facebook Messenger statistics</h1>
            </Box>

            <Grid container spacing={12}>
                <Grid item xs={4}>
                    <h2>Event log</h2>
                    <p>Information about operations in progress.</p>
                    <ul>
                        {logs.map(log => <li key={log.timestamp + log.message}>{logMap[log.message]}</li>)}
                    </ul>
                </Grid>
                <Grid item xs={8}>
                    <h2>Stat graphs</h2>
                    <p>When server finishes processing the part of metrics, graph will be displayed here.</p>

                    {stats.map(stat => getGraphForMetrics(stat))}
                </Grid>
            </Grid>
        </Container>
    );
}