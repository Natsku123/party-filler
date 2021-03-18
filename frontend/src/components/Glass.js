import React from 'react'
import { makeStyles } from '@material-ui/core/styles'

const useStyles = makeStyles((theme) => ({
    root: {
        background: "rgba(255,255,255,0.1)",
        borderRadius: "1em",
        position: "relative",
        backdropFilter: "blur(40px)",
        border: "solid 2px transparent",
        backgroundClip: "padding-box"
    }
}))

const Glass = (props) => {
    const classes = useStyles()
    return (
        <div className={classes.root}>
            {props.children}
        </div>
    )
}

export default Glass