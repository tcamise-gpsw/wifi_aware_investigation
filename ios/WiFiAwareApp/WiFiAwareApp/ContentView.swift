import SwiftUI

struct ContentView: View {
    @EnvironmentObject var appState: AppState
    @State private var isDiscovering = false

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Text("WiFi Aware POC")
                    .font(.largeTitle)
                    .fontWeight(.bold)

                // WiFi Aware Support Status
                HStack {
                    Image(systemName: appState.wifiAwareSupported ? "checkmark.circle.fill" : "xmark.circle.fill")
                        .foregroundColor(appState.wifiAwareSupported ? .green : .red)
                    Text(appState.wifiAwareSupported ? "WiFi Aware Supported" : "WiFi Aware Not Supported")
                        .font(.headline)
                }
                .padding()
                .background(appState.wifiAwareSupported ? Color.green.opacity(0.1) : Color.red.opacity(0.1))
                .cornerRadius(10)

                Text("Implementation Pending")
                    .font(.title3)
                    .foregroundColor(.secondary)

                Spacer()

                Button(action: {
                    if appState.wifiAwareSupported {
                        isDiscovering.toggle()
                        // TODO: Implement WiFi Aware discovery
                    }
                }) {
                    Text(isDiscovering ? "Stop Discovery" : "Start Discovery")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(appState.wifiAwareSupported ? (isDiscovering ? Color.red : Color.blue) : Color.gray)
                        .cornerRadius(10)
                }
                .disabled(!appState.wifiAwareSupported)
                .padding(.horizontal)

                Spacer()
            }
            .padding()
            .navigationTitle("WiFi Aware")
            .alert("WiFi Aware Not Supported", isPresented: $appState.showUnsupportedAlert) {
                Button("OK", role: .cancel) { }
            } message: {
                Text(appState.supportMessage)
            }
        }
    }
}

#Preview {
    ContentView()
        .environmentObject(AppState())
}
