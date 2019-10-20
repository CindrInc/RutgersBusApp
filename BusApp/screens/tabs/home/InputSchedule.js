import React from 'react';
import {
  Image,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  AsyncStorage,
  ActivityIndicator,
  TextInput,
  Picker
} from 'react-native';
import Colors from '../../../constants/Colors';
import Data from '../../../constants/Data';
import ModalDropdown from 'react-native-modal-dropdown';


export default class InputSchedule extends React.Component {
    numClasses = 4;

    constructor(props) {
        super(props)
        this.state = {
            schedule: [{}, {}, {}, {}]
        }
    }

    getClassInputComponent(idx) {
        return (
            <View key={idx} style={styles.classInput}>
                <Text style={styles.classNumber}>Class #{idx + 1}</Text>
                <View style={styles.inputContainer}>
                    <Text style={styles.inputName}>Name</Text>
                    <TextInput style={styles.textInput} onChangeText={(text) => {
                        let sched = this.state.schedule;
                        sched[idx].name = text;
                        this.setState({
                            schedule: sched
                        });
                    }}></TextInput>
                </View>
                <View style={styles.inputContainer}>
                    <Text style={styles.inputName}>Day of Week</Text>
                    <ModalDropdown
                        style={styles.dropdownInput}
                        textStyle={styles.dropdownText}
                        dropdownTextStyle={styles.dropdownMenuText}
                        options={['Monday/Wednesday', 'Tuesday/Thursday', 'Wednesday/Friday', 'Monday/Tuesday', 'Thursday/Friday']}
                        defaultIndex={0}
                        onSelect={(i, value) => {
                            let sched = this.state.schedule;
                            sched[idx].day = value;
                            this.setState({
                                schedule: sched
                            });
                        }
                    }/>
                </View>
                <View style={styles.inputContainer}>
                    <Text style={styles.inputName}>Start Time</Text>
                    <TextInput style={styles.textInput} onChangeText={(text) => {
                        let sched = this.state.schedule;
                        sched[idx].start = text;
                        this.setState({
                            schedule: sched
                        });
                    }}></TextInput>
                </View>
                <View style={styles.inputContainer}>
                    <Text style={styles.inputName}>End Time</Text>
                    <TextInput style={styles.textInput} onChangeText={(text) => {
                        let sched = this.state.schedule;
                        sched[idx].end = text;
                        this.setState({
                            schedule: sched
                        });
                    }}></TextInput>
                </View>
                <View style={styles.inputContainer}>
                    <Text style={styles.inputName}>Building Code</Text>
                    <ModalDropdown
                        style={styles.dropdownInput}
                        textStyle={styles.dropdownText}
                        dropdownTextStyle={styles.dropdownMenuText}
                        options={Data.buildings}
                        defaultIndex={0}
                        onSelect={(i, value) => {
                            let sched = this.state.schedule;
                            sched[idx].build = value;
                            this.setState({
                                schedule: sched
                            });
                        }
                    }/>
                </View>
            </View>
        )
    }

    render() {
        let classInputs = []
        for (let i = 0; i < this.numClasses; i++) {
            classInputs.push(this.getClassInputComponent(i))
        }
        return (
            <View style={styles.container}>
                <ScrollView>
                    <View style={styles.imageContainer}>
                        <Image style={styles.infoImage} source={require('../../../assets/images/schedule.png')}/>
                        <Text style={styles.infoText}>Input your schedule information from WebReg, using information like the above.</Text>
                    </View>
                    {classInputs}
                    <View style={styles.doneBtnContainer}>
                        <TouchableOpacity style={styles.doneBtn} onPress={this.onInputSchedule}>
                            <Text style={styles.doneTxt}>Done</Text>
                        </TouchableOpacity>
                    </View>
                </ScrollView>
            </View>
        )
    }

    onInputSchedule = async () => {
        let final = this.state.schedule;
        for (let i = 0; i < this.numClasses; i++) {
            let classInfo = this.state.schedule[i];
            if (!(classInfo.name &&  classInfo.day && classInfo.start && classInfo.end && classInfo.build)) {
                final = [];
            }
        }
        try {
            await AsyncStorage.setItem('schedule', JSON.stringify(final))
        } catch (err) {
            console.log(err)
        }
        this.props.navigation.pop()
    }
}

InputSchedule.navigationOptions = {
    header: null
};

const styles = StyleSheet.create({
    container: {
        flex: 1
    },
    infoImage: {
        width: 254 * 0.7,
        height: 162 * 0.7,
        marginBottom: 5
    },
    imageContainer: {
        marginTop: 40,
        display: 'flex',
        alignItems: 'center'
    },
    infoText: {
        textAlign: "center"
    },
    classInput: {
        padding: 4,
        marginBottom: 10
    },
    classNumber: {
        fontSize: 20,
        fontWeight: '600'
    },
    inputName: {
        fontSize: 18,
        marginTop: 3,
        marginRight: 3,
        width: 120
    },
    inputContainer: {
        display: 'flex',
        flexDirection: 'row',
        padding: 4
    },
    textInput: {
        borderWidth: 1,
        borderStyle: 'solid',
        borderColor: '#ccc',
        borderRadius: 10,
        padding: 5,
        flex: 1
    },
    dropdownInput: {
        borderWidth: 1,
        borderColor: '#ccc',
        borderRadius: 10,
        padding: 5,
        textAlign: "center",
        flex: 1
    },
    dropdownText: {
        fontSize: 15
    },
    dropdownMenuText: {
        fontSize: 15
    },
    doneBtnContainer: {
        display: 'flex',
        alignItems: 'center',
        marginBottom: 200
    },
    doneBtn: {
        borderWidth: 2,
        borderStyle: 'solid',
        borderColor: Colors.scarlet,
        borderRadius: 10,
        padding: 5,
        width: 60,
        marginTop: 20,
        marginBottom: 30
    },
    doneTxt: {
        textAlign: 'center',
        fontWeight: 'bold',
        color: Colors.scarlet
    }
})