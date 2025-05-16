import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtCharts 2.15

Item {
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 10

        Label {
            text: "Your Gaming Stats"
            font.pixelSize: 28
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Tracking since: " + dashboardController.trackingStartDate
            font.pixelSize: 16
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Total Playtime: " + dashboardController.totalPlaytime.toFixed(1) + " hours"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        ColumnLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 10

            Label {
                text: "Top Games"
                font.pixelSize: 18
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
            }

            Repeater {
                model: dashboardController.topGames
                Label {
                    text: modelData[0] + ": " + modelData[1].toFixed(1) + " hours"
                    font.pixelSize: 16
                    Layout.alignment: Qt.AlignHCenter
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 5

            Label {
                text: "Select Period: " + (slider.value === 0 ? "Today" : slider.value === dashboardController.maxIntervalDays ? "All Time" : slider.value + " days")
                font.pixelSize: 18
                Layout.alignment: Qt.AlignHCenter
            }

            Slider {
                id: slider
                from: 0
                to: dashboardController.maxIntervalDays
                value: 0
                stepSize: 1
                Layout.fillWidth: true
                onValueChanged: dashboardController.setIntervalDays(value)
            }
        }

        ChartView {
            width: 1100
            height: 500
            Layout.alignment: Qt.AlignHCenter
            antialiasing: true
            legend.visible: true
            legend.alignment: Qt.AlignRight
            legend.font.pixelSize: 18
            margins.right: 50

            PieSeries {
                id: pieSeries
                visible: dashboardController.pieChartData.length > 0 && dashboardController.pieChartData[0][0] !== "No Data"
                function updateSlices() {
                    console.log("Updating PieSeries, data:", JSON.stringify(dashboardController.pieChartData))
                    pieSeries.clear()
                    var data = dashboardController.pieChartData
                    for (var i = 0; i < data.length; i++) {
                        var name = data[i][0]
                        var hours = data[i][1]
                        var percent = dashboardController.totalPlaytime > 0 ? (hours / dashboardController.totalPlaytime * 100).toFixed(1) : 0
                        var label = name + ": " + hours.toFixed(1) + "h (" + percent + "%)"
                        var value = hours > 0 ? hours : 0.001
                        pieSeries.append(label, value)
                        pieSeries.at(i).color = name === "No Data" ? "#cccccc" : Qt.hsla(i / data.length, 0.7, 0.5, 1.0)
                        pieSeries.at(i).labelPosition = PieSlice.LabelOutside
                        pieSeries.at(i).labelFont.pixelSize = 10
                        pieSeries.at(i).labelArmLengthFactor = 0.3
                        pieSeries.at(i).labelVisible = true
                        pieSeries.at(i).borderWidth = 1
                        pieSeries.at(i).borderColor = "black"
                        console.log("Added slice:", label, value)
                    }
                }

                Component.onCompleted: {
                    updateSlices()
                }

                Connections {
                    target: dashboardController
                    function onIntervalChanged() {
                        pieSeries.updateSlices()
                    }
                }
            }

            Rectangle {
                visible: dashboardController.pieChartData.length === 0 || dashboardController.pieChartData[0][0] === "No Data"
                width: parent.width
                height: parent.height
                color: "white"

                Text {
                    anchors.centerIn: parent
                    text: "🎮 No gaming today! Time to play? 😄"
                    font.pixelSize: 16
                    color: "black"
                }
            }
        }

        Item {
            Layout.fillHeight: true
        }
    }
}