# from sqlalchemy import Table, Column, String, ForeignKey, Integer
# from models.base_model import Base
# from sqlalchemy.orm import relationship, Mapped, mapped_column
#
#
#
# class PlaceAmenity(Base):
#     """Association table for Place and Amenity."""
#     __tablename__ = "place_amenity"
#     place_id = Column(String(60), ForeignKey("places.city_id"), primary_key=True, nullable=False)
#     amenity_id = Column(String(60), ForeignKey("amenities.id"), primary_key=True, nullable=False)
#     # amenity = relationship("Amenity", back_populates="place_amenity")
#     # place = relationship("Place", back_populates="place_amenity")
#
# # association_table = Table(
# #     "place_amenity",
# #     Base.metadata,
# #     Column("place_id", String(60), ForeignKey("places.id"), primary_key=True, nullable=False),
# #     Column("amenity_id", String(60), ForeignKey("amenities.id"), primary_key=True, nullable=False)
# # )