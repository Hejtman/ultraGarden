TARGET  = ultraGarden
CXX     = g++
LFLAGS  = -L/usr/local/lib -lwiringPi -lcurl
WARNCXXFLAGS= -Wall -Wextra -Wshadow -Weffc++ -Wstrict-aliasing -ansi -pedantic
WARNLFLAGS  = 

EXTLIBS_OBJ	= extlib/c-log/src/log.o
SOURCES     = $(wildcard *.cpp) $(wildcard */*.cpp) 
OBJECTS     = $(SOURCES:.cpp=.o) $(EXTLIBS_OBJ)
DEPFILES    = $(SOURCES:.cpp=.d) $(EXTLIBS_OBJ:.o=.d)

BUILD	= debug
ifeq ($(BUILD),debug)
	CXXFLAGS= -g3 -ggdb -O0 -DDEBUG -std=gnu++14 -fstack-protector
else
	CXXFLAGS= -g3 -O3 -DDEBUG -std=gnu++14
endif


all: $(TARGET)
$(TARGET): $(OBJECTS)
	$(CXX) $(WARNCXXFLAGS) $(WARNLFLAGS) $(CFXXLAGS) -o $(TARGET) $(OBJECTS) $(LFLAGS)

%.o: %.cpp
	$(CXX) -MMD $(WARNCXXFLAGS) $(CXXFLAGS) -o $@ -c $<

extlib/c-log/src/log.o: extlib/c-log/src/log.c
	$(CXX) -MMD $(WARNCXXFLAGS) $(CXXFLAGS) -o $@ -c $<

clean:
	rm -f $(DEPFILES) $(OBJECTS) $(TARGET)

