TARGET  = ultraGarden
CXX     = g++
CFLAGS  = -O3 -DDEBUG -std=c++0x
LFLAGS  = -L/usr/local/lib -lwiringPi
LIBS    =
WARNCFLAGS  = -Wall -Wextra -Wshadow -Weffc++ -Wstrict-aliasing -ansi -pedantic -Werror
WARNLFLAGS  = 

SOURCES     = $(wildcard *.cpp) $(wildcard hw/*.cpp)
OBJECTS     = $(SOURCES:.cpp=.o)
DEPFILES    = $(SOURCES:.cpp=.d)

all: $(TARGET)
$(TARGET): $(OBJECTS)
	$(CXX) $(WARNCFLAGS) $(WARNLFLAGS) $(CFLAGS) -o $(TARGET) $(OBJECTS) $(LIBS) $(LFLAGS)

%.o: %.cpp
	$(CXX) -MMD $(WARNCFLAGS) $(CFLAGS) -o $@ -c $<

clean:
	rm -f $(DEPFILES) $(OBJECTS) $(TARGET)


