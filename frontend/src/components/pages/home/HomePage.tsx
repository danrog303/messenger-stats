import React, {FormEvent, useEffect, useRef, useState} from "react";
import axios, {AxiosProgressEvent} from "axios";
import {Box, Container, Grid} from "@mui/material";
import InputFileUpload from "../../shared/InputFileUpload";
import LinearProgressWithLabel from "../../shared/LinearProgressWithLabel";
import {useNavigate} from "react-router-dom";
import instruction from "../../../assets/instuction.svg"

import "./HomePage.css";

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
        <Container className={"container"}>
            <div className={"vertical-align"}>
            <Box>
                <h1 className={"title-name"}>Facebook Messenger statistics</h1>
            </Box>

            <Grid container spacing={12}>
                <Grid item xs={6}>
                    <p>
                        <h2 className={"left-title"}>How to use?</h2>
                    </p>
                    <div className={"image-container"}>
                        <img src={instruction} className={"instruction-icon"}></img>
                    </div>
                    <div>
                        <div className={"number-circle inline-points"}>1</div>
                        <div className={"inline-points"}> Open <a href={"https://accountscenter.facebook.com/info_and_permissions/dyi"}>Facebook data manager</a></div>
                    </div>
                    <div>
                        <div className={"number-circle inline-points"}>2</div>
                        <div className={"inline-points"}> Download your conversation data</div>
                    </div>
                    <div>
                        <div className={"number-circle inline-points"}>3</div>
                        <div className={"inline-points"}> Upload here and wait for your stats! </div>
                    </div>
                </Grid>
                <Grid item xs={6}>
                    <form>
                        <LinearProgressWithLabel value={progressPercentage}/>
                        <InputFileUpload handleFileChange={handleFile}
                                         accept="zip,application/octet-stream,application/zip,application/x-zip,application/x-zip-compressed"  />
                    </form>
                </Grid>
            </Grid>
            </div>
        </Container>
    );


}
