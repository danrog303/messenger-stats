import * as React from 'react';
import { styled } from '@mui/joy';
import {FileUploader} from "react-drag-drop-files";
import "./InputFileUpload.css";

interface InputFileUploadProps {
    accept?: string;
    handleFileChange: (file: File) => void;
}

export default function InputFileUpload(props: InputFileUploadProps) {
    return (
        <FileUploader
            handleChange={props.handleFileChange}
            name="file"
            types={["ZIP"]}
            label={"Upload a zip file with your data"}
            classes={"dragndrop"} />
    );
}