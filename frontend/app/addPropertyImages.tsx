import React, { useState } from "react";
import { Alert, StyleSheet, ScrollView, View, Text, TouchableOpacity, KeyboardAvoidingView, Platform } from "react-native";
import { useNavigation, useRoute, RouteProp } from "@react-navigation/native";
import Button from "./components/button";
import TextField from "./components/textField";
import CustomImagePicker from "./components/imagePicker";
import useAxios from "./hooks/useAxios";
import { Ionicons } from "@expo/vector-icons";
import { LandlordHomeStackParamList } from "./stacks/landlordHomeStack";
import { StackNavigationProp } from "@react-navigation/stack";

type LandlordHomeAddPropertyImageScreenRouteProp = RouteProp<LandlordHomeStackParamList, 'addPropertyImages'>;
type LandlordHomeAddPropertyImageScreenProp = StackNavigationProp<LandlordHomeStackParamList, 'addPropertyImages'>;

export default function AddPropertyImagesScreen() {
    const navigation = useNavigation<LandlordHomeAddPropertyImageScreenProp>();
    const route = useRoute<LandlordHomeAddPropertyImageScreenRouteProp>();
    const { post, error } = useAxios();
    const { propertyData } = route.params;

    const [images, setImages] = useState<{ label: string; image: string; description: string }[]>([]);
    const [loading, setLoading] = useState(false);

    const addImage = () => {
        if (images.length >= 10) {
            Alert.alert("Error", "You can only upload up to 10 images.");
            return;
        }
        setImages([...images, { label: "", image: "", description: "" }]);
    };

    const updateImage = (index: number, key: "label" | "image" | "description", value: string) => {
        const updatedImages = [...images];
        updatedImages[index][key] = value;
        setImages(updatedImages);
    };

    const handleSubmit = async () => {
        if (images.length === 0) {
            Alert.alert("Error", "You must add at least one image.");
            return;
        }

        for (let i = 0; i < images.length; i++) {
            const img = images[i];
            if (!img.label.trim() || !img.description.trim() || !img.image) {
                Alert.alert("Error", "All fields (Label, Description, and Image) must be filled.");
                return;
            }
        }

        setLoading(true);

        const processedImages = await Promise.all(
            images.map(async (img) => {
                const response = await fetch(img.image);
                const blob = await response.blob();
                const reader = new FileReader();
                reader.readAsDataURL(blob);
                return new Promise<{ label: string; image: string; description: string }>((resolve) => {
                    reader.onloadend = () => {
                        const base64Image = (reader.result as string).split(",")[1];
                        resolve({ ...img, image: base64Image });
                    };
                });
            })
        );

        const body = { ...propertyData, images: processedImages };
        const apiResponse = await post("/api/properties/", body);

        setLoading(false);
        if (apiResponse) {
            Alert.alert("Success", "Property created successfully!");
            navigation.pop(2);
        } else {
            Alert.alert("Error", "Failed to create property.");
        }
    };

    return (
        <KeyboardAvoidingView
            style={styles.container}
            behavior={Platform.OS === "ios" ? "padding" : "height"}
            keyboardVerticalOffset={Platform.OS === "ios" ? 100 : 70}
        >
            {/* Sticky Header */}
            <View style={styles.header}>
                <TouchableOpacity
                    style={styles.backButton}
                    onPress={() => navigation.goBack()}
                    disabled={loading}
                >
                    <Ionicons name="arrow-back" size={24} color="black" />
                </TouchableOpacity>
                <Text style={styles.headerText}>Upload Additional Property Images</Text>
            </View>

            <ScrollView
                contentContainerStyle={styles.scrollContent}
                keyboardShouldPersistTaps="handled"
            >
                {images.map((img, index) => (
                    <View key={index} style={styles.imageContainer}>
                        <TextField
                            placeholder="Label (e.g., Kitchen, Bedroom)"
                            value={img.label}
                            onChangeText={(text) => updateImage(index, "label", text)}
                            disabled={loading}
                        />
                        <View style={styles.fieldSpacing} />
                        <TextField
                            placeholder="Description"
                            value={img.description}
                            onChangeText={(text) => updateImage(index, "description", text)}
                            disabled={loading}
                        />
                        <View style={styles.fieldSpacing} />
                        <CustomImagePicker
                            image={img.image}
                            onImageSelected={(uri) => updateImage(index, "image", uri)}
                            disabled={loading}
                        />
                    </View>
                ))}

                <View style={styles.buttonContainer}>
                    <Button
                        text="Add Image"
                        onClick={addImage}
                        disabled={images.length >= 10 || loading}
                    />
                    <View style={styles.buttonSpacing} />
                    <Button
                        text={loading ? "Submitting..." : "Submit Property"}
                        onClick={handleSubmit}
                        disabled={loading}
                    />
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#f5f5f5"
    },
    header: {
        flexDirection: "row",
        alignItems: "center",
        paddingTop: 50,
        paddingBottom: 10,
        backgroundColor: "white",
        borderBottomWidth: 1,
        borderBottomColor: "#ddd",
        elevation: 3,
        zIndex: 100,
    },
    backButton: {
        paddingLeft: 15,
    },
    headerText: {
        fontSize: 22,
        fontWeight: "bold",
        flex: 1,
        textAlign: "center",
        paddingRight: 35,
    },
    scrollContent: {
        flexGrow: 1,
        paddingTop: 150, // 🔹 Ensures content doesn't overlap with sticky header
        paddingHorizontal: 16,
        paddingBottom: 20,
    },
    imageContainer: {
        marginBottom: 24, // Increased space between sections
    },
    fieldSpacing: {
        height: 10, // Adds margin between label, description, and image fields
    },
    buttonContainer: {
        marginTop: 0, // Adds margin above buttons
    },
    buttonSpacing: {
        height: 10, // Creates gap between Add Image & Submit buttons
    },
});