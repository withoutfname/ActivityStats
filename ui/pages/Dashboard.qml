import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtCharts 2.15

Item {
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20

        Label {
            text: "Your Gaming Stats"
            font.pixelSize: 28
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Tracking since: " + controller.trackingStartDate
            font.pixelSize: 16
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Total Playtime: " + controller.totalPlaytime.toFixed(1) + " hours"
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
                model: controller.topGames
                Label {
                    text: modelData[0] + ": " + modelData[1].toFixed(1) + " hours"
                    font.pixelSize: 16
                    Layout.alignment: Qt.AlignHCenter
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 10

            Label {
                text: "Select Period: " + (slider.value === 0 ? "Today" : slider.value === controller.maxIntervalDays ? "All Time" : slider.value + " days")
                font.pixelSize: 18
                Layout.alignment: Qt.AlignHCenter
            }

            Slider {
                id: slider
                from: 0
                to: controller.maxIntervalDays
                value: 0
                stepSize: 1
                Layout.fillWidth: true
                onValueChanged: controller.setIntervalDays(value)
            }
        }

        ChartView {
            width: 300
            height: 300
            Layout.alignment: Qt.AlignHCenter
            antialiasing: true
            backgroundColor: "#f0f0f0"
            legend.visible: true
            legend.alignment: Qt.AlignRight

            PieSeries {
                id: pieSeries
                function updateSlices() {
                    console.log("Updating PieSeries, data:", JSON.stringify(controller.pieChartData))
                    pieSeries.clear()
                    var data = controller.pieChartData
                    if (data.length === 0) {
                        pieSeries.append("No Data", 1.0)
                        pieSeries.at(0).color = "#cccccc"
                        console.log("No data, added fallback slice")
                        return
                    }
                    for (var i = 0; i < data.length; i++) {
                        var name = data[i][0]
                        var hours = data[i][1]
                        var percent = controller.totalPlaytime > 0 ? (hours / controller.totalPlaytime * 100).toFixed(1) : 0
                        var label = name + ": " + hours.toFixed(1) + "h (" + percent + "%)"
                        var value = hours > 0 ? hours : 0.001
                        pieSeries.append(label, value)
                        pieSeries.at(i).color = name === "No Data" ? "#cccccc" : Qt.hsla(i / data.length, 0.7, 0.5, 1.0)
                        console.log("Added slice:", label, value)
                    }
                }

                Component.onCompleted: {
                    updateSlices()
                }

                Connections {
                    target: controller
                    function onIntervalChanged() {
                        pieSeries.updateSlices()
                    }
                }
            }
        }

        Item {
            Layout.fillHeight: true
        }
    }
}