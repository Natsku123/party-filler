import React, { useState, useEffect } from 'react'
import {
  TextField,
  Button,
  Dialog,
  DialogActions,
  DialogTitle,
  DialogContent,
  DialogContentText
} from '@material-ui/core'
import {
  DateTimePicker,
  MuiPickersUtilsProvider,
} from '@material-ui/pickers'
import MomentUtils from '@date-io/moment';

import SplitButton from '../SplitButton'
import Glass from '../Glass'

import { partyService } from '../../services/parties'
import { playerService } from "../../services/players";
import { serverService } from "../../services/servers";
import {gameService} from "../../services/games";
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
    root: {
        position: "relative",
        backdropFilter: "blur(40px)",
        backgroundClip: "padding-box"
    },
    dialog: {
        backgroundColor: "#333333"
    }
}))

const PartyForm = (props) => {
  const classes = useStyles()
  const [ title, setTitle ] = useState('')
  const [ selectedChannel, setSelectedChannel ] = useState(0)
  const [ selectedGame, setSelectedGame ] = useState(0);
  const [ games, setGames ] = useState(null)
  const [ gNames, setGNames ] = useState([])
  const [ maxPlayers, setMaxPlayers ] = useState(5)
  const [ minPlayers, setMinPlayers ] = useState(5)
  const [ description, setDescription ] = useState('')
  const [ channelId, setChannelId ] = useState(5)
  const [ startTime, setStartTime ] = useState(new Date())
  const [ endTime, setEndTime ] = useState(new Date(startTime.getTime() + (60*60*1000)))

  const [ channels, setChannels ] = useState(null)
  const [ chNames, setChNames ] = useState(["No channel"]);
  const [ currentUser, setCurrentUser ] = useState(null);

  const [ newGameDialog, setNewGameDialog ] = useState(false);

  const [ newGameName, setNewGameName ] = useState("");
  const [ newGameSize, setNewGameSize ] = useState(5);

  useEffect(() => {
      let channelNames = ["No channel"]

      playerService.getCurrent().then(r => {
          setCurrentUser(r);
      }, e => {
          props.onError(e.response.data.detail);
      });

      playerService.getVisibleChannels().then(r => {
          r.forEach(c => {
              channelNames.push(c.server.name + " - " + c.name);
          });
          setChannels(r);
          setChNames(channelNames);
      }, e => {
          props.onError(e.response.data.detail);
      });
  }, [props])

  useEffect(() => {
      gameService.getAll().then(r => {
          let names = [];
          r.forEach(game => {
              names.push(game.name);
          })
          setGames(r);
          setGNames(names);
      }, e => {
          props.onError(e.response.data.detail);
      });
  }, [props])

  const createParty = (event) => {
    event.preventDefault()
    console.log(selectedChannel);
    let channelDetails;
    if (selectedChannel > 0) {
        channelDetails = channels[selectedChannel-1];
    } else {
        channelDetails = null;
    }

    let partyObject;
    if (channelDetails !== null) {
        console.log(channelDetails);
        setChannelId(channelDetails.id);

        partyObject = {
            title,
            leaderId: currentUser.id,
            gameId: games[selectedGame].id,
            channelId,
            maxPlayers,
            minPlayers,
            description,
            startTime,
            endTime,
        }
    } else {
        partyObject = {
            title,
            leaderId: currentUser.id,
            gameId: games[selectedGame].id,
            maxPlayers,
            minPlayers,
            description,
            startTime,
            endTime,
        }
    }

    partyService.create(partyObject).then(r => {
        props.onSuccess("Party " + r.title + " created.");
        setTitle('')
        setDescription('')
        setStartTime(new Date())
        setEndTime(new Date(startTime.getTime() + (60*60*1000)))
    }, e => {
        props.onError(e.response.data.detail);

    });



    // setChannelId(5)
  }

  const openNewGameDialog = () => {
    setNewGameDialog(true);
  }

  const closeNewGameDialog = () => {
    setNewGameDialog(false);
    setNewGameName("");
    setNewGameSize(5);
  }

  const changeGame = (game) => {
      setSelectedGame(game);
      const newCurrent = games[game];
      setMaxPlayers(newCurrent.defaultMaxPlayers);
      setMinPlayers(newCurrent.defaultMaxPlayers);
  }

  const createGame = () => {
    const newObject = {
        "name": newGameName,
        "defaultMaxPlayers": newGameSize
    };
    gameService.create(newObject).then(r => {
        props.onSuccess("Game " + r.name + " created.")
        const g = games;
        const gn = gNames;
        gn.push(r.name);
        g.push(r);
        setGames(g);
        setGNames(gn);
    }, e => {
        props.onError(e.response.data.detail)
    });
    closeNewGameDialog();
  }

  return (
    <div>
        <form onSubmit={createParty}>
            <div>
                <TextField label="title" value={title} onChange={({target}) => setTitle(target.value)}/>
            </div>
            <div>
                { channels ?
                    <div>
                        channel:
                        <SplitButton options={chNames} selected={selectedChannel} setSelected={setSelectedChannel}/>
                    </div> :
                    <div>loading channels...</div>
                }
            </div>
            <div>
                { games ?
                    <div>
                        game:
                        <SplitButton options={gNames} selected={selectedGame} setSelected={changeGame}/>
                    </div> :
                    <div>loading games...</div>
                }
                <div>
                    <Button variant="outlined" color="primary" onClick={openNewGameDialog}>New Game</Button>
                </div>
            </div>
            <div>
                <TextField label="Max Players" type='number' min='1' value={maxPlayers} onChange={({target}) => setMaxPlayers(Number(target.value))}/>
            </div>
            <div>
                <TextField label="Min Players" type='number' min='1' value={minPlayers} onChange={({target}) => setMinPlayers(Number(target.value))}/>
            </div>
            <div>
                <TextField label="Description" value={description} onChange={({target}) => setDescription(target.value)} multiline/>
            </div>
            <MuiPickersUtilsProvider utils={MomentUtils}>
                <div>
                    <DateTimePicker label="Start Time" value={startTime} onChange={setStartTime}/>
                </div>
                <div>
                    <DateTimePicker label="End Time" value={endTime} onChange={setEndTime}/>
                </div>
            </MuiPickersUtilsProvider>

            {/*
      <div>
        <TextField label="Channel Id" type='number' value={channelId} onChange={({target}) => setChannelId(target.value)}/>
      </div>
      */}
            <Button variant='contained' color='primary' type='submit'>Create Party</Button>
            <Dialog open={newGameDialog} onClose={closeNewGameDialog} aria-labelledby="form-dialog-title" className={classes.root}>
                <DialogTitle id="form-dialog-title" className={classes.dialog}>Create a new game</DialogTitle>
                <DialogContent className={classes.dialog}>
                    <DialogContentText>
                        To create a new game, give the name of the game and a default party maximum party size
                    </DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="game-name"
                        label="Name"
                        value={newGameName}
                        onChange={({target}) => setNewGameName(target.value)}
                        fullWidth
                    />
                    <TextField
                        margin="dense"
                        id="game-max-size"
                        label="Max Party size"
                        type="number"
                        value={newGameSize}
                        onChange={({target}) => setNewGameSize(Number(target.value))}
                        fullWidth
                    />
                </DialogContent>
                <DialogActions className={classes.dialog}>
                    <Button onClick={closeNewGameDialog} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={createGame} color="primary">
                        Create
                    </Button>
                </DialogActions>
            </Dialog>
        </form>
    </div>
  )
}

export default PartyForm
