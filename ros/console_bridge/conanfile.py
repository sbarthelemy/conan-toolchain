from conans import ConanFile, CMake, tools
import os
import glob

class ConsolebridgeConan(ConanFile):
    name = "console_bridge"
    version = "0.2.5"
    license = "BSD"
    url = "https://github.com/sbarthelemy/conan-toolchain"
    description = "A ROS-independent package for logging that seamlessly" \
                  " pipes into rosconsole/rosout for ROS-dependent packages."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = "Boost /1.59.0@lasote/stable"
    exports_sources = ["*.patch"]
    def source(self):
        git_tag = self.version
        self.run("git clone https://github.com/ros/console_bridge.git --branch %s" % git_tag)
        for p in glob.glob("*.patch"):
            self.output.info("applying patch \"{}\"".format(p))
            tools.patch(base_path="console_bridge", patch_file=p)
        tools.replace_in_file("console_bridge/CMakeLists.txt",
               "project(console_bridge)",
               "project(console_bridge)\n" \
               "include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\n" \
               "conan_basic_setup()")

    def imports(self):
       self.copy("*.dll", "", "bin")
       self.copy("*.dylib", "", "lib")

    def build(self):
        cmake = CMake(self)
        self.run('cmake console_bridge %s' % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst=".", src="console_bridge")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*-config.cmake", ".", ".")

    def package_info(self):
        self.cpp_info.libs = ["console_bridge"]
