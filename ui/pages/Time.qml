import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
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

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 5

            Label {
                text: timeController.startDate + " — " + timeController.endDate
                font.pixelSize: 18
                Layout.alignment: Qt.AlignHCenter
            }

            RangeSlider {
                id: rangeSlider
                from: 0
                to: timeController.maxIntervalDays
                first.value: 0
                second.value: 0
                stepSize: 1
                Layout.fillWidth: true
                first.onMoved: {
                    var newStart = Math.floor(first.value)
                    var newEnd = Math.floor(second.value)
                    if (newEnd - newStart < 5) {
                        newEnd = Math.min(newStart + 5, to)
                        second.value = newEnd
                    }
                    timeController.setIntervalRange(newStart, newEnd)
                }
                second.onMoved: {
                    var newStart = Math.floor(first.value)
                    var newEnd = Math.floor(second.value)
                    if (newEnd - newStart < 5) {
                        newStart = Math.max(newEnd - 5, from)
                        first.value = newStart
                    }
                    timeController.setIntervalRange(newStart, newEnd)
                }
            }
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 20

            Rectangle {
                width: 200
                height: 100
                color: "white"
                border.color: "black"
                border.width: 1
                radius: 10

                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: 5

                    Label {
                        text: "Total: " + timeController.totalPlaytime.toFixed(1) + "h"
                        font.pixelSize: 16
                        Layout.alignment: Qt.AlignHCenter
                    }

                    Label {
                        text: "Games: " + timeController.gameCount
                        font.pixelSize: 16
                        Layout.alignment: Qt.AlignHCenter
                    }
                }
            }
        }

        ColumnLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 10

            Label {
                text: "Stats for Selected Range"
                font.pixelSize: 18
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
            }

            Label {
                text: "Total Playtime: " + timeController.totalPlaytime.toFixed(1) + " hours"
                font.pixelSize: 16
                Layout.alignment: Qt.AlignHCenter
            }

            Label {
                text: "Average Session: " + timeController.averageSession.toFixed(1) + " hours"
                font.pixelSize: 16
                Layout.alignment: Qt.AlignHCenter
            }

            Label {
                text: "Daily Average Playtime: " + timeController.dailyAveragePlaytime.toFixed(1) + " hours"
                font.pixelSize: 16
                Layout.alignment: Qt.AlignHCenter
            }

            Label {
                text: "Max Session: " + timeController.maxSession[1].toFixed(1) + "h on " + timeController.maxSession[0] + " (" + timeController.maxSession[2] + ")"
                font.pixelSize: 16
                Layout.alignment: Qt.AlignHCenter
            }

            Label {
                text: "Max Game Session: " + timeController.maxGameSession[1].toFixed(1) + "h on " + timeController.maxGameSession[0] + " (" + timeController.maxGameSession[2] + ")"
                font.pixelSize: 16
                Layout.alignment: Qt.AlignHCenter
            }
        }

        Item {
            Layout.fillHeight: true
        }

        // Автоматически вызываем расчёт подинтервалов и Daytime Playtime при изменении диапазона
        Connections {
            target: timeController
            function onIntervalChanged() {
                var sessionData = timeController.averageSessionChartData
                var daytimeData = timeController.daytimePlaytime
                console.log("Average session data for subintervals: " + JSON.stringify(sessionData))
                console.log("Daytime playtime: " + JSON.stringify(daytimeData))
                console.log("Total Playtime in QML: " + timeController.totalPlaytime)
                console.log("Average Session in QML: " + timeController.averageSession)
                console.log("Daily Average Playtime in QML: " + timeController.dailyAveragePlaytime)
                console.log("Game Count in QML: " + timeController.gameCount)
            }
        }
    }
}