#include <iostream>
#include <vector>
#include <random>
#include <fstream>

// Structure to hold a mesh node point (X, Z coordinate)
struct Node {
    double x;
    double z; // Height profile coordinate
};

int main() {
    // 1. Simulation Parameters (Configured for Glasgow JWNC profiles)
    int num_points = 100;
    double junction_length = 200.0; // 200 nm slice
    double dx = junction_length / (num_points - 1);
    
    double target_thickness = 1.5;  // 1.5 nm nominal Al2O3 oxide thickness
    double rms_roughness = 0.15;    // 0.15 nm RMS roughness deviation

    // Setup Gaussian random distribution to model surface peaks and valleys
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<double> dist(0.0, rms_roughness);

    std::vector<Node> bottom_interface(num_points);
    std::vector<Node> top_interface(num_points);

    // 2. Open an output stream to generate raw numerical validation data
    std::ofstream outFile("junction_mesh.csv");
    outFile << "X,Z_Bottom,Z_Top,Local_Thickness\n";

    for (int i = 0; i < num_points; ++i) {
        double current_x = i * dx;
        
        // Inject randomized Gaussian roughness variations to both layers
        double roughness_bottom = dist(gen);
        double roughness_top = dist(gen);

        bottom_interface[i] = {current_x, roughness_bottom};
        top_interface[i] = {current_x, target_thickness + roughness_top};
        
        double local_thickness = top_interface[i].z - bottom_interface[i].z;

        // Write columns cleanly to the spreadsheet data file
        outFile << current_x << "," 
                << bottom_interface[i].z << "," 
                << top_interface[i].z << "," 
                << local_thickness << "\n";
    }

    outFile.close();
    std::cout << "[SUCCESS] Generated a rough Josephson junction profile data sheet!" << std::endl;
    return 0;
}

// Windows entry point wrapper required by 32-bit compiler configurations
#ifdef _WIN32
#include <windows.h>
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    return main();
}
#endif