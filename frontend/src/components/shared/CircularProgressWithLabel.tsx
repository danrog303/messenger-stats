import {Box, CircularProgress, CircularProgressProps, Typography} from "@mui/material";
import React from "react";

export default function CircularProgressWithLabel(
    props: CircularProgressProps & { value: number },
) {
    return (
        <Box sx={{ position: 'relative', display: 'inline-flex' }}>
            <CircularProgress variant="determinate" {...props} />
            <Box
                sx={{
                    top: 0,
                    left: 0,
                    bottom: 0,
                    right: 0,
                    position: 'absolute',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                <Typography variant="caption" component="div">
                    <span>{`${Math.round(props.value)}%`}</span>
                </Typography>
            </Box>
        </Box>
    );
}
