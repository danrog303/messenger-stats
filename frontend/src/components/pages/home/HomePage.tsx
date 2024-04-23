import React, {FormEvent, useState} from "react";
import axios, {AxiosProgressEvent} from "axios";
import {Box, Container, Grid} from "@mui/material";
import InputFileUpload from "../../shared/InputFileUpload";
import LinearProgressWithLabel from "../../shared/LinearProgressWithLabel";
import {useNavigate} from "react-router-dom";

export default function HomePage () {
    const navigate = useNavigate();
    const [progressPercentage, setProgressPercentage] = useState(0);

    const handleFile = (event: FormEvent) => {
        event.preventDefault();
        const target = event.target as HTMLInputElement;
        if (target === null || target.files === null) {
            throw new Error("Form not found");
        }

        const file = target.files[0];
        const formData = new FormData();
        formData.append("file", file);
        axios.post("http://localhost:8080/upload", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
            onUploadProgress: (event: AxiosProgressEvent) => {
                setProgressPercentage(Math.round(100 * event.loaded) / event?.total!);
            },
        }).then(data => {
            navigate("/stats/" + data.data);
        });
    };

    return (
        <Container>
            <Box>
                <h1>Facebook Messenger statistics</h1>
            </Box>

            <Grid container spacing={12}>
                <Grid item xs={6}>
                    <p>
                        <strong>You have to download your FB data!</strong>
                    </p>
                    <div>
                        Here we will place a GIF graphic that will present how to get your
                        Facebook data.
                    </div>
                </Grid>
                <Grid item xs={6}>
                    <form>
                        <LinearProgressWithLabel value={progressPercentage} />
                        <InputFileUpload handleFileChange={handleFile}
                                         accept="zip,application/octet-stream,application/zip,application/x-zip,application/x-zip-compressed"  />
                    </form>
                </Grid>
            </Grid>
        </Container>
    );


}
