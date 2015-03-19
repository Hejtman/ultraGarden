TARGET  = ultraGarden
CXX     = g++
CFLAGS  = -O3 -DDEBUG
CXXFLAGS= -O3 -DDEBUG -std=c++11
LFLAGS  = -L/usr/local/lib -lwiringPi -lcurl
LIBS    =
WARNCFLAGS  = -Wall -Wextra -Wshadow -Weffc++ -Wstrict-aliasing -ansi -pedantic
WARNCXXFLAGS= -Wall -Wextra -Wshadow -Wstrict-aliasing -ansi -pedantic
WARNLFLAGS  = 

EXTLIBS_OBJ	= extlib/c-log/src/log.o
SOURCES     = $(wildcard *.cpp) $(wildcard */*.cpp) 
OBJECTS     = $(SOURCES:.cpp=.o) $(EXTLIBS_OBJ)
DEPFILES    = $(SOURCES:.cpp=.d) $(EXTLIBS_OBJ:.o=.d)

all: $(TARGET)
$(TARGET): $(OBJECTS)
	$(CXX) $(WARNCFLAGS) $(WARNLFLAGS) $(CFLAGS) -o $(TARGET) $(OBJECTS) $(LIBS) $(LFLAGS)

%.o: %.cpp
	$(CXX) -MMD $(WARNCXXFLAGS) $(CXXFLAGS) -o $@ -c $<

%.o: %.c
	$(CXX) -MMD $(WARNCFLAGS) $(CFLAGS) -o $@ -c $<

clean:
	rm -f $(DEPFILES) $(OBJECTS) $(TARGET)

