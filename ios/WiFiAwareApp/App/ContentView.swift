import SwiftUI

struct ContentView: View {
    @State private var isDiscovering = false

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Text("WiFi Aware POC")
                    .font(.largeTitle)
                    .fontWeight(.bold)

                Text("Implementation Pending")
                    .font(.title3)
                    .foregroundColor(.secondary)

                Spacer()

                Button(action: {
                    isDiscovering.toggle()
                    // TODO: Implement WiFi Aware discovery
                }) {
                    Text(isDiscovering ? "Stop Discovery" : "Start Discovery")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(isDiscovering ? Color.red : Color.blue)
                        .cornerRadius(10)
                }
                .padding(.horizontal)

                Spacer()
            }
            .padding()
            .navigationTitle("WiFi Aware")
        }
    }
}

#Preview {
    ContentView()
}
