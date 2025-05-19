import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {

    Component.onCompleted: {
        rangeSlider.first.value = 0
        rangeSlider.second.value = timeController.maxIntervalDays
        timeController.setIntervalRange(0, timeController.maxIntervalDays)
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 10

        Label {
            text: "Time Stats"
            font.pixelSize: 28
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        RangeSlider {
            id: rangeSlider
            from: 0
            to: timeController.maxIntervalDays
            first.value: 0
            second.value: 25
            stepSize: 1
            Layout.fillWidth: true
            snapMode: RangeSlider.SnapAlways
            first.onMoved: timeController.setIntervalRange(Math.floor(first.value), Math.floor(second.value))
            second.onMoved: timeController.setIntervalRange(Math.floor(first.value), Math.floor(second.value))
        }

        Label {
            text: {
                var start = Qt.formatDate(new Date(timeController.startDate), "dd-MM-yyyy");
                var end = Qt.formatDate(new Date(timeController.endDate), "dd-MM-yyyy");
                return "Period: " + start + " to " + end
            }
            font.pixelSize: 18
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Total Playtime: " + timeController.simpTotalPlaytime + " hours"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Average Session Time: " + timeController.avgSessionTime + " hours"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Average Day Playtime: " + timeController.avgDayPlaytime.toFixed(1) + " hours"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Total Sessions: " + timeController.simpSessionCount
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Max Session Duration: " + timeController.maxSessionDuration[0].toFixed(1) + " hours (Date: " + timeController.maxSessionDuration[2] + ", Game: " + timeController.maxSessionDuration[1] + ")"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Max Daily Game Session: " + timeController.maxDailyGameSession[0].toFixed(1) + " hours (Date: " + timeController.maxDailyGameSession[1] + ", Game: " + timeController.maxDailyGameSession[2] + ", Sessions: " + timeController.maxDailyGameSession[3] + ")"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Max Daily Total Duration: " + timeController.maxDailyTotalDuration[0].toFixed(1) + " hours (Date: " + timeController.maxDailyTotalDuration[1] + ", Games: " + timeController.maxDailyTotalDuration[2] + ")"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Connections {
            target: timeController
            function onIntervalChanged() {
                console.log("Interval changed, updating UI")
            }
        }

        Item {
            Layout.fillHeight: true
        }
    }
}